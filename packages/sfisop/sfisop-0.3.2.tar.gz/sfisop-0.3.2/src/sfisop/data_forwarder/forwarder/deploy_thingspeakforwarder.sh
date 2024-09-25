#! /bin/bash
echo "Starting Thingspeak forwarder"
echo $1

cd ..
pwd

export PYTHONPATH=$(pwd):$(pwd)/forwarder/datamodels/
echo $PYTHONPATH

cd forwarder
pwd

python3 thingspeak/thingspeak_forwarder.py --configfile $1
