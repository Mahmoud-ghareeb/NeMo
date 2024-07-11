Requirements
------------

* Python 3.10 or above
* Pytorch 1.13.1 or above
* NVIDIA GPU (if you intend to do model training)

Developer Documentation
-----------------------

.. |main| image:: https://readthedocs.com/projects/nvidia-nemo/badge/?version=main
  :alt: Documentation Status
  :scale: 100%
  :target: https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/

.. |stable| image:: https://readthedocs.com/projects/nvidia-nemo/badge/?version=stable
  :alt: Documentation Status
  :scale: 100%
  :target:  https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/stable/

+---------+-------------+------------------------------------------------------------------------------------------------------------------------------------------+
| Version | Status      | Description                                                                                                                              |
+=========+=============+==========================================================================================================================================+
| Latest  | |main|      | `Documentation of the latest (i.e. main) branch. <https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/>`_                  |
+---------+-------------+------------------------------------------------------------------------------------------------------------------------------------------+
| Stable  | |stable|    | `Documentation of the stable (i.e. most recent release) branch. <https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/stable/>`_ |
+---------+-------------+------------------------------------------------------------------------------------------------------------------------------------------+

Install NeMo Framework
----------------------

Build from Source
^^^^^^^^^^^^^^^^^

If you want to clone the NeMo GitHub repository and contribute to NeMo open-source development work, use the following installation method:

.. code-block:: bash

    conda create -n nemo_lm python==3.11
    conda activate nemo_lm

.. code-block:: bash

    apt-get update && apt-get install -y libsndfile1 ffmpeg
    git clone https://github.com/Mahmoud-ghareeb/NeMo.git
    cd NeMo
    ./reinstall.sh

If you only want the toolkit without the additional Conda-based dependencies, you can replace ``reinstall.sh`` with ``pip install -e .`` when your PWD is the root of the NeMo repository.

KenLM
^^^^

to install the LM do the following.

Run the following code:

.. code-block:: bash

  ./install_beamsearch_decoders.sh

RNNT
^^^^

For optimal performance of a Recurrent Neural Network Transducer (RNNT), install the Numba package from Conda.

Run the following code:

.. code-block:: bash

  conda remove numba
  pip uninstall numba
  conda install -c conda-forge numba


Future Work
-----------

The NeMo Framework Launcher does not currently support ASR and TTS training, but it will soon.

Discussions Board
-----------------

FAQ can be found on the NeMo `Discussions board <https://github.com/NVIDIA/NeMo/discussions>`_. You are welcome to ask questions or start discussions on the board.

Contribute to NeMo
------------------

We welcome community contributions! Please refer to `CONTRIBUTING.md <https://github.com/NVIDIA/NeMo/blob/stable/CONTRIBUTING.md>`_ for the process.

Publications
------------------

We provide an ever-growing list of `publications <https://nvidia.github.io/NeMo/publications/>`_ that utilize the NeMo Framework.

To contribute an article to the collection, please submit a pull request to the ``gh-pages-src`` branch of this repository. For detailed information, please consult the README located at the `gh-pages-src branch <https://github.com/NVIDIA/NeMo/tree/gh-pages-src#readme>`_.

Licenses
--------

* `NeMo GitHub Apache 2.0 license <https://github.com/NVIDIA/NeMo?tab=Apache-2.0-1-ov-file#readme>`__

* NeMo is licensed under the `NVIDIA AI PRODUCT AGREEMENT <https://www.nvidia.com/en-us/data-center/products/nvidia-ai-enterprise/eula/>`__. By pulling and using the container, you accept the terms and conditions of this license.
