import argparse
import os
from decouple import config
import yaml


class BrokerConfig:
    def __init__(self, username, password, broker_url, broker_port, client_id, topic, qos, get_timeout):
        self.USERNAME = username
        self.PASSWORD = password
        self.BROKER_URL = broker_url
        self.BROKER_PORT = broker_port
        self.CLIENT_ID = client_id
        self.TOPIC = topic
        self.QOS = qos
        self.QUEUE_GET_TIMEOUT = get_timeout

    def __str__(self) -> str:
        return ''.join((f'Configuration: \n',
                        f'TOPIC: {self.TOPIC}:{self.QOS} \n',
                        f'BROKER: {self.BROKER_URL}:{self.BROKER_PORT} \n'
                        f'CLIENTID: {self.CLIENT_ID}'))


class ForwarderConfigurationException(Exception):
    pass


def get_broker_config(config_file: str) -> BrokerConfig:

    try:
        BROKER_USERNAME = config('BROKER_USERNAME')
        BROKER_PASSWORD = config('BROKER_PASSWORD')

    except Exception as e:
        raise ForwarderConfigurationException(f"Error when reading credentials from environment: {e}")

    # load broker configuration

    try:
        with open(config_file) as f:
            conf = yaml.load(f, Loader=yaml.FullLoader)
            BROKER_URL = conf['BROKER_URL']
            BROKER_PORT = conf['BROKER_PORT']
            CLIENT_ID = conf['CLIENT_ID']
            BROKER_TOPIC = conf['BROKER_TOPIC']
            QOS = conf['QOS']
            QUEUE_GET_TIMEOUT = conf['QUEUE_GET_TIMEOUT']

    except Exception as e:
        raise ForwarderConfigurationException(f"Error when reading from config file: {e}")

    broker_config = BrokerConfig(BROKER_USERNAME, BROKER_PASSWORD,
                                 BROKER_URL, BROKER_PORT, CLIENT_ID,
                                 BROKER_TOPIC, QOS,  QUEUE_GET_TIMEOUT)

    return broker_config


def get_forwarder_configfile(description: str) -> str:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--configfile", required=True, help="Path to the config file")
    args = parser.parse_args()

    if not os.path.exists(args.configfile):
        raise ForwarderConfigurationException(f"Error: The configfile '{args.configfile}' does not exist.")

    return args.configfile

