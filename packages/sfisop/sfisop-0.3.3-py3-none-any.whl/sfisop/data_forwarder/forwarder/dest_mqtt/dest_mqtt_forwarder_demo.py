import logging
from logging.handlers import TimedRotatingFileHandler

#import forwarder.dest_mqtt.dest_mqtt_utils as utils
#from forwarder.dest_mqtt.dest_mqtt_config import DestMQTTConfig
#from forwarder.dest_mqtt.dest_mqtt_client import DestMQTTClient
#from forwarder.dest_mqtt.dest_mqtt_forwarder import DstMQTTForwarder

from . import dest_mqtt_utils as utils
from .dest_mqtt_config import DestMQTTConfig
from .dest_mqtt_client import DestMQTTClient
from .dest_mqtt_forwarder import DstMQTTForwarder


class DemoClient(DestMQTTClient):
    """
    An MQTT client class for the forwarded destination
    """

    def __init__(self, demo_config: DestMQTTConfig, llogger):

        super().__init__(demo_config, llogger)
        # Do something else here if necessary
        self.unique_id: list = []
        self.identifiers: list = []

    def forward_all(self, ts_data_str: object) -> object:
        """
        This is an example parsing the incoming datastring and passing it on in a different format.
        :param ts_data_str:
        :return:
        """
        data_points = utils.get_fields(ts_data_str, self.PARAMETER_FIELD)

        for timestr, sensor, metadata in data_points:  # find list of unique identifiers
            self.logger.info(
                f'DemoClient: recieved update for {sensor["identifier"], sensor["entity"]}, ts = {timestr}')
            if not sensor['identifier'] in self.identifiers:
                self.identifiers.append(sensor['identifier'])

        for ids in self.identifiers:
            for timestr, sensor, metadata in data_points:
                if sensor['identifier'] == ids:
                    s_id = sensor["name"]
                    state_topic = f"demotopic/sensor/{s_id}/state"
                    # Add entity to json message for state update
                    entity = sensor['entity']
                    state = sensor['value']
                    state_str = '{' + f' "{entity}": {state}' + '}'

                    self.dest_mqtt_client.publish(state_topic, state_str, qos=2, retain=True)
        return True


if __name__ == '__main__':
    '''
    This is an example model client. It will subscribe to topics from the smartocean platform 
    and forward them to another MQTT service. You will need an appropriate client class like the one above which 
    handles formatting messages before forwarding to your local MQTT service.
    Populate the forward_all method with code appropriate for your destination.
    '''

    forwarder_config = DestMQTTConfig.get_dest_mqtt_forwarder_config_cmdargs("MQTT Forwarder to MQTT")

    formatter = logging.Formatter(fmt='%(asctime)s[%(levelname)s]:%(message)s', datefmt="%H:%M:%S")

    logger = logging.getLogger("MQTT Forwarder Rotating Log")
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(forwarder_config.logfile, when="m", interval=30, backupCount=5)

    handler.setFormatter(formatter)
    # logging.getLogger().handlers.clear()
    logger.addHandler(handler)

    logger.info('MQTT Forwarder to MQTT')
    logger.info(str(forwarder_config))

    # logger.propagate = False # FIXME: to avoid multiple log outputs

    try:
        client = DemoClient(forwarder_config.FWDCONFIG, logger)
        forwarder = DstMQTTForwarder(forwarder_config, logger, client=client)
        forwarder.run()

    except Exception as e:
        logger.error(f'Unhandled exception: {e}')
