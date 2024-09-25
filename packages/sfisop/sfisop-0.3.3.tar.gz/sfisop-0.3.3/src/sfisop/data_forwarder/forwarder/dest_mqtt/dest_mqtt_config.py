import yaml

from ..forwarder_config import BrokerConfig, ForwarderConfigurationException, get_broker_config, \
    get_forwarder_configfile


class DestMQTTConfig:
    """
    Forwarding to another MQTT server
    """

    def __init__(self, host, port, c_id, do_forward, parameter_field, site_name):
        """
        :param host: Hostname of the destination MQTT server to forward to
        :param port: Port number of the destination MQTT server to forward to
        :param c_id: Client ID to use (must be unique)
        :param do_forward: 
        :param parameter_field: 
        :param site_name: 
        """
        self.DO_FORWARD = do_forward
        self.host = host
        self.port = port
        self.client_id = c_id
        self.PARAMETER_FIELD = parameter_field
        self.SITE_NAME = site_name

    def __str__(self):
        return f'Do Forward: {self.DO_FORWARD}\nParameter Field: {self.PARAMETER_FIELD}'

    @staticmethod
    def get_dst_mqtt_config(config_file: str):
        try:
            with open(config_file) as f:
                conf = yaml.load(f, Loader=yaml.FullLoader)

                DST_MQTT_BROKER_HOST = conf['DST_MQTT_BROKER_HOST']
                DST_MQTT_BROKER_PORT = conf['DST_MQTT_BROKER_PORT']
                DST_MQTT_BROKER_ID = conf['DST_MQTT_BROKER_ID']
                PARAMETER_FIELD = conf['PARAMETER_FIELD']
                DO_FORWARD = conf['DO_FORWARD']
                SITE_NAME = conf['SITE_NAME']

        except Exception as e:
            raise ForwarderConfigurationException(f"Error when reading from config file: {e}")

        fwd_config = DestMQTTConfig(DST_MQTT_BROKER_HOST, DST_MQTT_BROKER_PORT, DST_MQTT_BROKER_ID, DO_FORWARD,
                                    PARAMETER_FIELD, SITE_NAME)

        return fwd_config

    @staticmethod
    def get_dest_mqtt_forwarder_config(config_file):
        try:
            with open(config_file) as f:
                conf = yaml.load(f, Loader=yaml.FullLoader)
                LOG_FILE = conf['LOG_FILE']

        except Exception as e:
            raise ForwarderConfigurationException(f"Error when reading from config file: {e}")

        broker_config = get_broker_config(config_file)
        fwd_config = DestMQTTConfig.get_dst_mqtt_config(config_file)
        forwarder_config = ForwarderConfig(broker_config, fwd_config, LOG_FILE)
        return forwarder_config

    @staticmethod
    def get_dest_mqtt_forwarder_config_cmdargs(description: str):
        config_file = get_forwarder_configfile(description)
        forwarder_config = DestMQTTConfig.get_dest_mqtt_forwarder_config(config_file)
        return forwarder_config


class ForwarderConfig:
    def __init__(self, broker_config: BrokerConfig, fwd_config: DestMQTTConfig, logfile: str):
        self.BROKERCONFIG = broker_config
        self.FWDCONFIG = fwd_config
        self.logfile = logfile

    def __str__(self):
        return f'{self.BROKERCONFIG}\n{self.FWDCONFIG}\nLogFile: {self.logfile}'
