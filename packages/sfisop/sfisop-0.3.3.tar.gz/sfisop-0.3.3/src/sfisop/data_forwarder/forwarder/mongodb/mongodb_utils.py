import datetime
import logging


def convert_time(ts_data_data_json):
    try:
        ts_data_data_time = ts_data_data_json['time']
        date_time = datetime.datetime.fromisoformat(ts_data_data_time)
        ts_data_data_json['time'] = date_time
        return ts_data_data_json
    except Exception as e:
        logging.error("Convert time error: " + str(e))
        return None


def extract_data(ts_data_json):
    try:
        return ts_data_json['data']
    except Exception as e:
        logging.error("Extract data error: " + str(e))
