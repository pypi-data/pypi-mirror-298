import argparse
from decouple import config
import yaml

import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler

#from forwarder.mqtt_forwarder import MQTTForwarder, BrokerConfig
from ..mqtt_forwarder import MQTTForwarder, BrokerConfig

#from forwarder.mongodb.mongodb_client import MongoDBClient
#from forwarder.mongodb.mongodb_config import MongoDBForwarderConfig, get_mongodb_forwarder_config_cmdargs

from .mongodb_client import MongoDBClient
from .mongodb_config import MongoDBForwarderConfig, get_mongodb_forwarder_config_cmdargs


#from forwarder.datamodels.tsdatamodel.tsdata_utils import validate_ts_json_data
from ....datamodels.tsdatamodel.tsdata_utils import validate_ts_json_data


class MongoDBForwarder(MQTTForwarder):

    def __init__(self, forwarder_config: MongoDBForwarderConfig, logger):

        super().__init__(forwarder_config.BROKERCONFIG, logger)

        self.mongodb_client = MongoDBClient(forwarder_config.MONGODBCONFIG, logger)
        self.do_forward = forwarder_config.MONGODBCONFIG.DO_FORWARD

    def ensure_mongodb_connection(self): # FIXME: it this function used?
        try:
            self.mongodb_client.ping()
            return True
        except Exception as e:
            self.log(f'MongoDB connection error: {e}')
            return False

    def forward(self, in_message):

        self.log(f'MongoDBForwarder forward\n {in_message}')

        try:
            validate_ts_json_data(in_message)
        except Exception as e:
            self.log(f"MongoDB Forwarder in_message error: {e}")
            return

        if self.do_forward:

            self.log(f'Client forwarding enabled\n')

            try:
                res = self.mongodb_client.insert(in_message) # FIXME: handle return value

            except Exception as e:
                self.log(f'Error forwarding to MongoDB: {e}')
                raise

        else:
            self.log(f'Client forwarding disabled.\n')


if __name__ == '__main__':

    forwarder_config = get_mongodb_forwarder_config_cmdargs("MongoDB forwarder")

    formatter = logging.Formatter(fmt='%(asctime)s[%(levelname)s]:%(message)s', datefmt="%H:%M:%S")

    logger = logging.getLogger("MongoDB Forwarder Rotating Log")
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(forwarder_config.logfile, when="m", interval=30, backupCount=5)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info('MongoDB Forwarder')
    logger.info(str(forwarder_config))

    try:
        forwarder = MongoDBForwarder(forwarder_config, logger)
        forwarder.run()

    except Exception as e:
        logger.error(f'Unhandled exception: {e}')
