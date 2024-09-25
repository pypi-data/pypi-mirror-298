import queue
import signal
from abc import abstractmethod

from paho.mqtt.client import CallbackAPIVersion, Client, ssl

#from forwarder.forwarder_config import BrokerConfig
from .forwarder_config import BrokerConfig


class MQTTForwarder:

    def __init__(self, broker_config: BrokerConfig, logger):

        self.CORE_USERNAME = broker_config.USERNAME
        self.CORE_PASSWORD = broker_config.PASSWORD
        self.CLIENT_ID = broker_config.CLIENT_ID

        try:
            self.subscriber = Client(CallbackAPIVersion.VERSION1, client_id=self.CLIENT_ID)
        except Exception as e:
            self.log(f"Error when creating paho client: {e}")

        self.BROKER_URL = broker_config.BROKER_URL
        self.BROKER_PORT = broker_config.BROKER_PORT

        self.TOPIC = broker_config.TOPIC

        self.QOS = broker_config.QOS

        self.QUEUE_GET_TIMEOUT = broker_config.QUEUE_GET_TIMEOUT

        self.do_continue = True
        self.msg_queue = queue.Queue()

        self.logger = logger

    def __str__(self) -> str:
        return ''.join((f'MQTT Forwarder Configuration: \n',
                        f'TOPIC: {self.TOPIC}:{self.QOS} \n',
                        f'BROKER: {self.BROKER_URL}:{self.BROKER_PORT} \n',
                        f'CLIENTID: {self.CLIENT_ID}'))

    def on_subscriber_connect(self, client, userdata, flags, rc):
        self.log(f'Subscriber [connected:{rc}]')
        client.subscribe(self.TOPIC, self.QOS)
        self.log("Subscriber [subscribed]")

    def on_subscriber_receive(self, client, userdata, message):

        ts_data_json_str = (str(message.payload.decode("utf-8")))

        self.log(f'Subscriber {self.CLIENT_ID} [received] [{ts_data_json_str[0:100]}]')

        self.msg_queue.put(ts_data_json_str)

    def subscriber_run(self):

        self.subscriber.on_message = self.on_subscriber_receive
        self.subscriber.on_connect = self.on_subscriber_connect

        self.subscriber.tls_set(tls_version=ssl.PROTOCOL_TLS)
        self.subscriber.username_pw_set(self.CORE_USERNAME, self.CORE_PASSWORD)

        self.subscriber.connect(host=self.BROKER_URL, port=self.BROKER_PORT, keepalive=120)

        #self.receiver.loop_forever()
        self.subscriber.loop_start()

    @abstractmethod
    def forward(self, in_message=None):
        pass

    # on graceful termination
    # https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully

    def interrupt_handler(self, *args):
        self.log("int_gracefully ...")
        self.do_continue = False

    # kill <pid> | kill -9 will not trigger handler
    def termination_gracefully(self, *args):
        self.log("term_gracefully ...")
        self.do_continue = False

    def log(self, msg: str):
        self.logger.info(msg)

    def run(self):

        signal.signal(signal.SIGINT, self.interrupt_handler)
        signal.signal(signal.SIGTERM, self.termination_gracefully)

        self.log('Starting Forwarder')
        self.log(self.__str__())

        self.subscriber_run()

        self.log('Subscriber running')

        while self.do_continue:

            try:

                self.log('Forwarder [Queue:wait]')
                in_message = self.msg_queue.get(timeout=self.QUEUE_GET_TIMEOUT)
                self.log(f'Forwarder [Queue:forward]')

                self.forward(in_message)

                self.log(f'Forwarder [Queue:forwarded]')

            except queue.Empty:
                self.log("Queue[empty]")

        self.log('Stopping subscriber')

        self.subscriber.loop_stop()

        self.log("Forwarder stopped")
