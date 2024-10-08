#!/usr/bin/env bash

shopt -s expand_aliases

NEMO_PATH=$(pwd)
if [ "$#" -eq 1 ]; then
  NEMO_PATH=$1
fi
KENLM_MAX_ORDER=10

if [ -d "$NEMO_PATH" ]; then
  echo "The folder '$NEMO_PATH' exists."
else
  echo "Error: The folder '$NEMO_PATH' does not exist. Specify it as a first command line positional argument!"
  exit 1
fi
cd $NEMO_PATH

if [ $(id -u) -eq 0 ]; then
  alias aptupdate='apt-get update'
  alias b2install='./b2'
else
  alias aptupdate='sudo apt-get update'
  alias b2install='sudo ./b2'
fi

aptupdate && apt-get upgrade -y && apt-get install -y swig liblzma-dev && rm -rf /var/lib/apt/lists/* # liblzma needed for flashlight decoder

# install Boost package for KenLM
wget https://boostorg.jfrog.io/artifactory/main/release/1.80.0/source/boost_1_80_0.tar.bz2 --no-check-certificate && tar --bzip2 -xf $NEMO_PATH/boost_1_80_0.tar.bz2 && cd boost_1_80_0 && ./bootstrap.sh && b2install --layout=tagged link=static,shared threading=multi,single install -j4 && cd .. || echo FAILURE
export BOOST_ROOT=$NEMO_PATH/boost_1_80_0

git clone https://github.com/NVIDIA/OpenSeq2Seq
cd OpenSeq2Seq
git checkout ctc-decoders
cd ..
mv OpenSeq2Seq/decoders $NEMO_PATH/
rm -rf OpenSeq2Seq
cd $NEMO_PATH/decoders
cp $NEMO_PATH/scripts/installers/setup_os2s_decoders.py ./setup.py
./setup.sh

cd $NEMO_PATH/decoders/kenlm/build && cmake -DKENLM_MAX_ORDER=$KENLM_MAX_ORDER .. && make -j2
cd $NEMO_PATH/decoders/kenlm
python setup.py install --max_order=$KENLM_MAX_ORDER
export KENLM_LIB=$NEMO_PATH/decoders/kenlm/build/bin
export KENLM_ROOT=$NEMO_PATH/decoders/kenlm
cd ..

#setup the folder
cd $NEMO_PATH
mkdir ../checkpoints
mkdir ../kenlm_binaries
mv test_model.ipynb ../
