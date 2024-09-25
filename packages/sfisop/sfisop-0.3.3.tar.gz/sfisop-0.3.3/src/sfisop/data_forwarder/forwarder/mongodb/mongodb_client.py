from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# https://stackoverflow.com/questions/68123923/pymongo-ssl-certificate-verify-failed-certificate-verify-failed-unable-to-ge
# python -m pip install pymongo
# Create a new client and connect to the server
# client = MongoClient(mac_uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection

# test data point for smart ocean data format

import logging
import certifi
import datetime
import json
import yaml

#import forwarder.mongodb.mongodb_utils as utils
from . import mongodb_utils as utils

from decouple import config

#from forwarder.mongodb.mongodb_config import MongoDBConfig
from .mongodb_config import MongoDBConfig

class MongoDBClient:

    def __init__(self, mongodb_config: MongoDBConfig, logger):

        self.cluster = mongodb_config.MONGO_DB_CLUSTER
        self.database_name = mongodb_config.MONGODB_DATABASE_NAME
        self.collection_name = mongodb_config.MONGODB_COLLECTION_NAME

        self.MONGO_DB_USER = mongodb_config.MONGO_DB_USER
        self.MONGO_DB_PASSWORD = mongodb_config.MONGO_DB_PASSWORD

        self.uri = f'mongodb+srv://{self.MONGO_DB_USER}:{self.MONGO_DB_PASSWORD}@{self.cluster}'

        self.client = None
        self.logger = logger


    def log(self, msg: str):
        self.logger.info(msg)

    def connect(self):

        try:
            self.client = MongoClient(
                self.uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
            return True
        except Exception as e:
            self.log("Connection error: " + str(e))
            return False

    def insert(self, ts_data_str):

        # TODO: add proper validation including isoformat.
        try:
            ts_data = json.loads(ts_data_str)
        except ValueError as e:
            self.log("JSON decoding error: " + str(e))
            return False

        ts_data_points = utils.extract_data(ts_data)

        if not self.connect():
            self.log("Failed to connect to MongoDB.")
            return False

        try:
            db = self.client[self.database_name]
        except Exception as e:
            self.log("Database error: " + str(e))
            self.disconnect()
            return False
        try:
            collection = db[self.collection_name]
        except Exception as e:
            self.log("Collection error: " + str(e))
            self.disconnect()
            return False

        try:

            self.log(f'Inserting data points: {len(ts_data_points)}')

            for ts_data_point in ts_data_points:

                self.log(f'Inserting\n {ts_data_point}')

                data_point = utils.convert_time(ts_data_point)

                if not data_point:
                    self.log("Failed to convert time.")
                else:
                    res = collection.insert_one(data_point) # FIXME: collect and use return value

                    self.log("Successfully inserted into " + self.collection_name + " collection.")

            self.log(f'Successfully inserted data points')

            self.disconnect()

            return True

        except Exception as e:
            self.log("Insert error: " + str(e))
            self.log("Error occurred during insert_one: " + str(e))
            self.disconnect()
            return False

    def disconnect(self):
        self.client.close()
        self.log('Disconnected')

    def ping(self):

        self.connect()

        try:
            self.client.admin.command('ping')
            self.log(
                "Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            self.log(str(e))
            return False

        self.disconnect()

        return True
