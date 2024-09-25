#! /bin/bash
echo "Starting MongoDB forwarder"
echo $1

cd ..
pwd

export PYTHONPATH=$(pwd):$(pwd)/forwarder/datamodels/
echo $PYTHONPATH

cd forwarder
pwd

python3 mongodb/mongodb_forwarder.py --configfile $1
