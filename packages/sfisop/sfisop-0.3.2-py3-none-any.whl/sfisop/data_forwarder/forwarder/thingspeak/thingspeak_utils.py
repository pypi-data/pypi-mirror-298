import json
import datetime

def get_fields(ts_data_str, parameter_field):

    CHANNEL_FIELD_MAX = 8 # Thingspeak channel can have up to 8 field

    ts_data = json.loads(ts_data_str)

    data = ts_data['data']

    data_points = list()

    for datapoint in data:

        observations = datapoint['observations']

        time_str = datapoint['time']  # TODO: should validate that it is iso format

        values = [None for _ in range(CHANNEL_FIELD_MAX)]

        for obs in observations:

            source_id = obs['source_id']

            if source_id in parameter_field:

                parameters = parameter_field[source_id]
                parameter = obs['parameter']

                if parameter in parameters:
                    field_no = parameters[parameter]
                    values[field_no-1] = float(obs['value'])

        data_points.append((time_str, values))

    # temporary fix to handle wsense nodes with 2 data points differing only in milliseconds
    if len(data_points) == 2:

        t0 = datetime.datetime.fromisoformat(data_points[0][0]).strftime('%Y-%m-%dT%H:%M:%S+%z')
        t1 = datetime.datetime.fromisoformat(data_points[1][0]).strftime('%Y-%m-%dT%H:%M:%S+%z')

        if t0 == t1:
            data_points[0] = (data_points[0][0],
                              [data_points[0][1][i] if data_points[0][1][i] is not None else data_points[1][1][i]
                               for i in range(CHANNEL_FIELD_MAX)])

            data_points.pop()

    return data_points


def get_time(ts_data_str):

    ts_data = json.loads(ts_data_str)

    data = ts_data['data'][0]

    time_str = data['time']  # TODO: should validate that it is iso format

    return time_str
