import argparse
import os
from decouple import config
import yaml

#from forwarder.forwarder_config import BrokerConfig, ForwarderConfigurationException, get_broker_config, get_forwarder_configfile
from ..forwarder_config import BrokerConfig, ForwarderConfigurationException, get_broker_config, get_forwarder_configfile

class MongoDBConfig:

    def __init__(self, username, password, cluster, database, collection, do_forward):

        self.MONGO_DB_USER = username
        self.MONGO_DB_PASSWORD = password

        self.MONGO_DB_CLUSTER = cluster
        self.MONGODB_DATABASE_NAME = database
        self.MONGODB_COLLECTION_NAME = collection
        self.DO_FORWARD = do_forward

    def __str__(self):
        return f'Cluster: {self.MONGO_DB_CLUSTER}\nDatabase: {self.MONGODB_DATABASE_NAME}\nCollection: {self.MONGODB_COLLECTION_NAME}\nDo Forward: {self.DO_FORWARD}'


class MongoDBForwarderConfig:
    def __init__(self, broker_config: BrokerConfig, mongodb_config: MongoDBConfig, logfile: str):
        self.BROKERCONFIG = broker_config
        self.MONGODBCONFIG = mongodb_config
        self.logfile = logfile

    def __str__(self):
        return f'{self.BROKERCONFIG}\n{self.MONGODBCONFIG}\nLogFile: {self.logfile}'


def get_mongodb_config(config_file: str) -> MongoDBConfig:

        try:
            with open(config_file) as f:
                conf = yaml.load(f, Loader=yaml.FullLoader)
                MONGO_DB_USER = config('MONGO_DB_USER')
                MONGO_DB_PASSWORD = config('MONGO_DB_PASSWORD')
                CLUSTER = conf['MONGO_DB_CLUSTER']
                DATABASE = conf['MONGODB_DATABASE_NAME']
                COLLECTION = conf['MONGODB_COLLECTION_NAME']
                DO_FORWARD = conf['DO_FORWARD']

        except Exception as e:
            raise ForwarderConfigurationException(f"Error when reading from config file: {e}")

        mongodb_config = MongoDBConfig(MONGO_DB_USER, MONGO_DB_PASSWORD, CLUSTER, DATABASE, COLLECTION, DO_FORWARD)

        return mongodb_config


def get_mongodb_forwarder_config(config_file) -> MongoDBForwarderConfig:

        try:
            with open(config_file) as f:
                conf = yaml.load(f, Loader=yaml.FullLoader)
                LOG_FILE = conf['LOG_FILE']

        except Exception as e:
            raise ForwarderConfigurationException(f"Error when reading from config file: {e}")

        broker_config = get_broker_config(config_file)

        mongodb_config = get_mongodb_config(config_file)

        forwarder_config = MongoDBForwarderConfig(broker_config, mongodb_config, LOG_FILE)

        return forwarder_config


def get_mongodb_forwarder_config_cmdargs(description: str) -> MongoDBForwarderConfig:

    config_file = get_forwarder_configfile(description)

    forwarder_config = get_mongodb_forwarder_config(config_file)

    return forwarder_config


