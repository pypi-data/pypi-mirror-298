#from forwarder.mqtt_forwarder import MQTTForwarder
#from forwarder.dest_mqtt.dest_mqtt_client import DestMQTTClient
#from forwarder.dest_mqtt.dest_mqtt_config import ForwarderConfig

from ..mqtt_forwarder import MQTTForwarder
from .dest_mqtt_client import DestMQTTClient
from .dest_mqtt_config import ForwarderConfig

#from tsdatamodel.tsdata_utils import validate_ts_json_data
from ....datamodels.tsdatamodel.tsdata_utils import validate_ts_json_data


class DstMQTTForwarder(MQTTForwarder):
    """
    Generic MQTT forwarder to forward from SFISO platform to another MQTT server.
    Override the forward() method for application specific formatting of the content
    """

    def __init__(self, forwarder_config_init: ForwarderConfig, llogger, client: DestMQTTClient = None):
        """

        :type forwarder_config_init: object
        """
        super().__init__(forwarder_config_init.BROKERCONFIG, llogger)

        self.forwarder_config = forwarder_config_init

        self.do_forward = forwarder_config_init.FWDCONFIG.DO_FORWARD
        if client is None:
            self.dst_client = DestMQTTClient(forwarder_config_init.FWDCONFIG, llogger)
        else:
            self.dst_client = client

    def forward(self, in_message):

        # self.log(f'DstMQTTForwarder forward\n {in_message}')
        self.log(f'DstMQTTForwarder forward')

        try:
            validate_ts_json_data(in_message)
        except Exception as fe:
            self.log(f"DstMQTTForwarder Forwarder in_message error: {fe}")
            return

        if self.do_forward:
            # self.log(f'Client forwarding enabled\n')
            try:
                self.log(f'DstMQTTForwarder forwarder in : {in_message}')
                self.dst_client.forward_all(in_message)
                self.log(f'DstMQTTForwarder forwarder forwarded')

            except Exception as fe:
                self.log(f'Error forwarding to DstMQTTForwarder: {fe}')
                raise

        else:
            self.log(f'Client forwarding disabled.\n')

    def run(self):
        self.dst_client.dest_mqtt_client.connect(self.dst_client.dest_mqtt_config.host,
                                                 self.dst_client.dest_mqtt_config.port)
        self.dst_client.dest_mqtt_client.loop_start()

        super().run()
        self.dst_client.dest_mqtt_client.loop_stop()
