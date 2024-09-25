#! /bin/bash

tail -f log-wsense1-mongodb-prod.log log-wsense2-mongodb-prod.log mongodb/log-virtualnode-mongodb-prod.log mongodb/log-aadinode-south-mongodb-prod.log
