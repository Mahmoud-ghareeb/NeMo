Requirements
------------

* Python 3.10 or above
* Pytorch 1.13.1 or above
* NVIDIA GPU (if you intend to do model training)

Install NeMo Framework With Beam Search
----------------------

1. Build from Source
^^^^^^^^^^^^^^^^^

If you want to clone the NeMo GitHub repository and contribute to NeMo open-source development work, use the following installation method:

.. code-block:: bash

    conda create -n nemo_lm python==3.10.12
    conda activate nemo_lm

.. code-block:: bash

    apt-get update && apt-get install -y libsndfile1 ffmpeg
    git clone https://github.com/Mahmoud-ghareeb/NeMo.git
    cd NeMo
    pip install -e .

2. Beam Search Decoders
^^^^

to install the LM do the following.

Run the following code:

.. code-block:: bash

    sh install_beamsearch_decoders.sh

after this, you will have in your base the following files/folders
1. checkpoints
2. kenlm_binaries
3. NeMo
4. test_model.ipynb

3. Kenlm
^^^^

to generate the LM do the following

1. copy your text file to => NeMo/decoders/kenlm/build/
2. cd into => NeMo/decoders/kenlm/build/

3. Run the following code:

.. code-block:: bash

    #change data.txt to your file name
    bin/lmplz -o 5 <data.txt >text.arpa
    bin/build_binary text.arpa text.binary

4. copy the generated "text.binary" into the "kenlm_binaries" folder

.. code-block:: bash

    #suggested command
    cp text.binary ../../../../kenlm_binaries/

4. Test the model
^^^^

Now Read The test_model.ipynb file and adjust it according to your data and paths ...

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
