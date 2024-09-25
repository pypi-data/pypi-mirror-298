import argparse
import os
from decouple import config
import yaml

from ..forwarder_config import BrokerConfig, ForwarderConfigurationException, get_broker_config, get_forwarder_configfile


class ThingsPeakConfig:

    def __init__(self, thingspeak_api_key, do_forward, parameter_field):
        self.THINGSPEAK_API_KEY = thingspeak_api_key
        self.DO_FORWARD = do_forward
        self.PARAMETER_FIELD = parameter_field

    def __str__(self):
        return f'Do Forward: {self.DO_FORWARD}\nParameter Field: {self.PARAMETER_FIELD}'


class ThingsPeakForwarderConfig:
    def __init__(self, broker_config: BrokerConfig, thingspeak_config: ThingsPeakConfig, logfile: str):
        self.BROKERCONFIG = broker_config
        self.THINGSPEAKCONFIG = thingspeak_config
        self.logfile = logfile

    def __str__(self):
        return f'{self.BROKERCONFIG}\n{self.THINGSPEAKCONFIG}\nLogFile: {self.logfile}'


def get_thingspeak_config(config_file: str) -> ThingsPeakConfig:

        try:
            with open(config_file) as f:
                conf = yaml.load(f, Loader=yaml.FullLoader)
                THINGSPEAK_CHANNEL_API_KEY = config(conf['THINGSPEAK_CHANNEL_API_KEY'])
                PARAMETER_FIELD = conf['PARAMETER_FIELD']
                DO_FORWARD = conf['DO_FORWARD']

        except Exception as e:
            raise ForwarderConfigurationException(f"Error when reading from config file: {e}")

        thingspeak_config = ThingsPeakConfig(THINGSPEAK_CHANNEL_API_KEY, DO_FORWARD, PARAMETER_FIELD)

        return thingspeak_config


def get_thingspeak_forwarder_config(config_file) -> ThingsPeakForwarderConfig:

        try:
            with open(config_file) as f:
                conf = yaml.load(f, Loader=yaml.FullLoader)
                LOG_FILE = conf['LOG_FILE']

        except Exception as e:
            raise ForwarderConfigurationException(f"Error when reading from config file: {e}")

        broker_config = get_broker_config(config_file)

        thingspeak_config = get_thingspeak_config(config_file)

        forwarder_config = ThingsPeakForwarderConfig(broker_config, thingspeak_config, LOG_FILE)

        return forwarder_config


def get_thingspeak_forwarder_config_cmdargs(description: str) -> ThingsPeakForwarderConfig:

    config_file = get_forwarder_configfile(description)

    forwarder_config = get_thingspeak_forwarder_config(config_file)

    return forwarder_config

