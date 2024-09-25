from abc import abstractmethod

import paho.mqtt.client as paho

#from forwarder.dest_mqtt.dest_mqtt_config import DestMQTTConfig
from .dest_mqtt_config import DestMQTTConfig


class DestMQTTClient:

    def __init__(self, dest_mqtt_config: DestMQTTConfig, logger):

        self.PARAMETER_FIELD = dest_mqtt_config.PARAMETER_FIELD
        self.logger = logger
        self.dest_mqtt_config = dest_mqtt_config

        #  MQTT mosquitto broker for relay
        try:
            self.dest_mqtt_client = paho.Client(paho.CallbackAPIVersion.VERSION2,
                                                client_id=self.dest_mqtt_config.client_id)
        except Exception as e:
            self.logger.error(f"Error when creating ha forward client: {e}")

        @self.dest_mqtt_client.connect_callback()
        def on_connect(client, userdata, flags, reason_code, properties):
            self.logger.info(f"Connected  with result code {reason_code}\n")

        @self.dest_mqtt_client.disconnect_callback()
        def on_disconnect(client, userdata, flags, reason_code, properties):
            self.logger.info(f"Disonnected with result code {reason_code}\n")

    @abstractmethod
    def forward_all(self, ts_data_str: object) -> object:
        pass
