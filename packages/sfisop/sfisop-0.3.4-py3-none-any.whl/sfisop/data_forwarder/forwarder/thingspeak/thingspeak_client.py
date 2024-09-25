import requests
import time
import json

#import forwarder.thingspeak.thingspeak_utils as utils
#from forwarder.thingspeak.thingspeak_config import ThingsPeakConfig

from . import thingspeak_utils as utils
from .thingspeak_config import ThingsPeakConfig


class ThingsPeakClient:

    def __init__(self, thingspeak_config: ThingsPeakConfig, logger):

        self.THINGSPEAK_API_KEY = thingspeak_config.THINGSPEAK_API_KEY
        self.PARAMETER_FIELD = thingspeak_config.PARAMETER_FIELD
        self.logger = logger

    URL = "https://api.thingspeak.com/update"

    HEADERS = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    def forward_iter(self, ts_data_str):

        values = utils.get_fields(ts_data_str, self.PARAMETER_FIELD)

        for i in range(0, len(values)):

            payload = f'api_key={self.THINGSPEAK_API_KEY}&field{i+1}={values[i]}'

            self.logger.info(f'ThingsPeak Client request with: {values[i]}')

            time.sleep(30)  # temporary fix to limit the number of API CALLS - we should switch to bulk write

            response = requests.request("POST", self.URL, headers=self.HEADERS, data=payload)

            self.logger.info(f'ThingsPeak Client response : {response} {response.text}')

        return True

    def forward_all(self, ts_data_str):

        URL_ALL = "https://api.thingspeak.com/update.json"

        headers = {'Content-Type': 'application/json'}

        data_points = utils.get_fields(ts_data_str, self.PARAMETER_FIELD)

        for values in data_points:

            if all(v is None for v in values[1]):
                self.logger.info(f'ThingsPeak Client Forward All is None: {values}')
                return False
            else:
                payload = json.dumps({
                    "api_key": self.THINGSPEAK_API_KEY,
                    "created_at": values[0],
                    "field1": values[1][0],
                    "field2": values[1][1],
                    "field3": values[1][2],
                    "field4": values[1][3],
                    "field5": values[1][4],
                    "field6": values[1][5],
                    "field7": values[1][6],
                    "field8": values[1][7]
                })

                self.logger.info(f'ThingsPeak Client request with: {payload}')

                self.logger.info(f'ThingsPeak Client waiting to limit API calls')

                time.sleep(30) # Limit API calls

                response = requests.request("POST", URL_ALL, headers=headers, data=payload)

                self.logger.info(f'ThingsPeak Client response : {response} {response.text}')

            return True
