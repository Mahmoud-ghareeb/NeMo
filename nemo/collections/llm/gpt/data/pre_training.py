from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import pytorch_lightning as pl
from pytorch_lightning.utilities.types import EVAL_DATALOADERS, TRAIN_DATALOADERS
from torch.utils import data
from torch.utils.data import DataLoader

from nemo.lightning.pytorch.plugins import MegatronDataSampler

if TYPE_CHECKING:
    from megatron.core.datasets.gpt_dataset import GPTDatasetConfig

    from nemo.collections.common.tokenizers.tokenizer_spec import TokenizerSpec


class PreTrainingDataModule(pl.LightningDataModule):
    def __init__(
        self,
        paths: Path | List[Path],
        weights: Optional[List[float]] = None,
        seq_length: int = 2048,
        tokenizer: Optional["TokenizerSpec"] = None,
        micro_batch_size: int = 4,
        global_batch_size: int = 8,
        rampup_batch_size: Optional[List[int]] = None,
        num_train_samples: int = 10_000,
        num_val_samples: int = 10_000,
        num_test_samples: int = 10_000,
        num_workers: int = 8,
        pin_memory: bool = True,
        persistent_workers: bool = False,
        reset_position_ids: bool = False,
        reset_attention_mask: bool = False,
        eod_mask_loss: bool = False,
        seed: int = 1234,
        split: str = "900,50,50",
        index_mapping_dir: Optional[str] = None,
    ) -> None:
        super().__init__()
        if not isinstance(paths, (list, tuple)):
            paths = [paths]
        if weights is not None:
            assert len(weights) == len(paths)
            if len(weights) == 1:
                # weights must be None if there is only one dataset
                weights = None

        self.paths = paths
        self.weights = weights
        self.seq_length = seq_length
        self.tokenizer = tokenizer
        self.num_train_samples = num_train_samples
        self.num_val_samples = num_val_samples
        self.num_test_samples = num_test_samples
        self.num_workers = num_workers
        self.pin_memory = pin_memory
        self.persistent_workers = persistent_workers
        self.reset_position_ids = reset_position_ids
        self.reset_attention_mask = reset_attention_mask
        self.eod_mask_loss = eod_mask_loss
        self.seed = seed
        self.split = split
        self.index_mapping_dir = index_mapping_dir
        self.init_global_step = 0

        from nemo.collections.nlp.modules.common.tokenizer_utils import get_nmt_tokenizer

        self.tokenizer = tokenizer or get_nmt_tokenizer("megatron", "GPT2BPETokenizer")
        self.data_sampler = MegatronDataSampler(
            seq_len=self.seq_length,
            micro_batch_size=micro_batch_size,
            global_batch_size=global_batch_size,
            rampup_batch_size=rampup_batch_size,
        )

    def setup(self, stage: str = "") -> None:
        from megatron.core.datasets.blended_megatron_dataset_builder import BlendedMegatronDatasetBuilder
        from megatron.core.datasets.gpt_dataset import GPTDataset

        assert (
            hasattr(self, "trainer") and self.trainer is not None
        ), "Setup should be completed when trainer and config are attached."

        # Trainer API
        max_train_steps = self.trainer.max_steps
        assert max_train_steps > 0, "Please specify trainer.max_steps"
        eval_iters = (max_train_steps // self.trainer.val_check_interval + 1) * self.trainer.limit_val_batches
        test_iters = self.trainer.limit_test_batches
        num_train_samples = int(max_train_steps * self.data_sampler.global_batch_size)
        num_val_samples = int(eval_iters * self.data_sampler.global_batch_size)
        num_test_samples = int(test_iters * self.data_sampler.global_batch_size)

        if self.trainer.limit_val_batches <= 1.0 and isinstance(self.trainer.limit_val_batches, float):
            # This is to make sure we only have one epoch on every validation iteration
            num_val_samples = None if self.weights is None else 1

        train_valid_test_num_samples = [num_train_samples, num_val_samples, num_test_samples]
        self._train_ds, self._validation_ds, self._test_ds = BlendedMegatronDatasetBuilder(
            GPTDataset,
            train_valid_test_num_samples,
            is_built_on_rank=lambda: True,
            config=self.gpt_dataset_config,
        ).build()

    # uncomment once fabric API is merged
    # def fabric_setup(
    #     self,
    #     fabric: fl.Fabric,
    #     num_train_samples: int,
    #     num_val_samples: int,
    #     num_test_samples: int,
    # ) -> None:
    #     from megatron.core.datasets.blended_megatron_dataset_builder import BlendedMegatronDatasetBuilder
    #     from megatron.core.datasets.gpt_dataset import GPTDataset
    #
    #     del fabric
    #     train_valid_test_num_samples = [num_train_samples, num_val_samples, num_test_samples]
    #     self._train_ds, self._validation_ds, self._test_ds = BlendedMegatronDatasetBuilder(
    #         GPTDataset, train_valid_test_num_samples, self.gpt_dataset_config,
    #     ).build()

    def train_dataloader(self) -> TRAIN_DATALOADERS:
        return self._create_dataloader(self._train_ds)

    def val_dataloader(self) -> EVAL_DATALOADERS:
        return self._create_dataloader(self._validation_ds)

    def test_dataloader(self) -> EVAL_DATALOADERS:
        return self._create_dataloader(self._test_ds)

    def _create_dataloader(self, dataset, **kwargs) -> DataLoader:
        self.init_global_step = self.trainer.global_step
        return DataLoader(
            dataset,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
            persistent_workers=self.persistent_workers,
            collate_fn=getattr(dataset, 'collate_fn', data.dataloader.default_collate),
            **kwargs,
        )

    @property
    def gpt_dataset_config(self) -> "GPTDatasetConfig":
        from megatron.core.datasets.gpt_dataset import GPTDatasetConfig

        return GPTDatasetConfig(
            blend=[[str(path) for path in self.paths], self.weights],
            random_seed=self.seed,
            sequence_length=self.seq_length,
            tokenizer=self.tokenizer,
            split=self.split,
            path_to_cache=self.index_mapping_dir,
            reset_position_ids=self.reset_position_ids,
            reset_attention_mask=self.reset_attention_mask,
            eod_mask_loss=self.eod_mask_loss,
        )

    def state_dict(self) -> Dict[str, Any]:
        """Called when saving a checkpoint, implement to generate and save datamodule state.

        Returns:
            A dictionary containing datamodule state.

        """
        consumed_samples = self.data_sampler.compute_consumed_samples(self.trainer.global_step - self.init_global_step)
        return {'consumed_samples': consumed_samples}

    def load_state_dict(self, state_dict: Dict[str, Any]) -> None:
        """Called when loading a checkpoint, implement to reload datamodule state given datamodule stat

        Args:
            state_dict: the datamodule state returned by ``state_dict``.

        """
        try:
            from apex.transformer.pipeline_parallel.utils import _GLOBAL_NUM_MICROBATCHES_CALCULATOR
        except ModuleNotFoundError:
            from nemo.lightning.apex_utils import _GLOBAL_NUM_MICROBATCHES_CALCULATOR
        consumed_samples = state_dict['consumed_samples']
        self.data_sampler.init_consumed_samples = consumed_samples
        self.data_sampler.prev_consumed_samples = consumed_samples
        num_microbatch_calculator = _GLOBAL_NUM_MICROBATCHES_CALCULATOR  # noqa: SLF001

        num_microbatch_calculator.update(
            consumed_samples=consumed_samples,
            consistency_check=False,
        )
        current_global_batch_size = num_microbatch_calculator.current_global_batch_size
        '''pl_module.log(
            "global_batch_size",
            current_global_batch_size,
            prog_bar=True,
            rank_zero_only=True,
            batch_size=1,
        )'''
        self.if_first_step = 1
