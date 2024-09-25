
import logging
from logging.handlers import TimedRotatingFileHandler

#from forwarder.mqtt_forwarder import MQTTForwarder
from ..mqtt_forwarder import MQTTForwarder

#from forwarder.thingspeak.thingspeak_client import ThingsPeakClient
#from forwarder.thingspeak.thingspeak_config import ThingsPeakForwarderConfig, get_thingspeak_forwarder_config_cmdargs

from .thingspeak_client import ThingsPeakClient
from .thingspeak_config import ThingsPeakForwarderConfig, get_thingspeak_forwarder_config_cmdargs

#from forwarder.datamodels.tsdatamodel.tsdata_utils import validate_ts_json_data
from ....datamodels.tsdatamodel.tsdata_utils import validate_ts_json_data


class ThingsPeakForwarder(MQTTForwarder):

    def __init__(self, forwarder_config: ThingsPeakForwarderConfig, logger):

        super().__init__(forwarder_config.BROKERCONFIG, logger)
        self.thingspeak_client = ThingsPeakClient(forwarder_config.THINGSPEAKCONFIG, logger)

        self.do_forward = forwarder_config.THINGSPEAKCONFIG.DO_FORWARD

    def forward(self, in_message):

        self.log(f'ThingsPeak forward\n {in_message}')

        try:
            validate_ts_json_data(in_message)
        except Exception as e:
            self.log(f"ThingsPeak Forwarder in_message error: {e}")
            return

        if self.do_forward:

            self.log(f'Client forwarding enabled\n')

            try:
                self.log(f'ThingsPeak forwarder in : {in_message}')
                self.thingspeak_client.forward_all(in_message)
                self.log(f'ThingsPeak forwarder forwarded')

            except Exception as e:
                self.log(f'Error forwarding to ThingsPeak: {e}')
                raise

        else:
            self.log(f'Client forwarding disabled.\n')


if __name__ == '__main__':

    forwarder_config = get_thingspeak_forwarder_config_cmdargs("ThingsPeak Forwarder")

    formatter = logging.Formatter(fmt='%(asctime)s[%(levelname)s]:%(message)s', datefmt="%H:%M:%S")

    logger = logging.getLogger("MQTT ThingsPeak Forwarder Rotating Log")
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(forwarder_config.logfile, when="m", interval=30, backupCount=5)

    handler.setFormatter(formatter)
    # logging.getLogger().handlers.clear()
    logger.addHandler(handler)

    logger.info('ThingsPeak Forwarder')
    logger.info(str(forwarder_config))

    #logger.propagate = False # FIXME: to avoid multiple log outputs

    try:
        forwarder = ThingsPeakForwarder(forwarder_config, logger)
        forwarder.run()

    except Exception as e:
        logger.error(f'Unhandled exception: {e}')