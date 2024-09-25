import json
import logging


def get_fields(ts_data_str, parameter_field):
    ts_data = json.loads(ts_data_str)
    data = ts_data['data']
    data_points = list()
    metadata = ts_data['metadata']

    for datapoint in data:
        metadata_dp = metadata
        metadata_dp.update(datapoint['location'])
        metadata_dp.update({"source": datapoint['source']})
        metadata_dp.update({"source_id": datapoint['source_id']})

        observations = datapoint['observations']
        time_str = datapoint['time']  # TODO: should validate that it is iso format
        metadata_dp.update({"timestamp": time_str})

        # columns: dict = {'time': [dp.time]}
        # columns['longitude'] = [dp.location.longitude]
        # columns['latitude']  = [dp.location.latitude]
        for obs in observations:
            sensor: dict = {}
            sensor['name'] = obs['source'].replace(' ', '_').replace('#', '')
            sensor['entity'] = obs['parameter'].replace(' ', '_').replace('#', '')
            sensor['unit'] = obs['unit']
            if (sensor['unit'] == 'DegC') or (sensor['unit'] == 'Deg.C'):
                sensor['unit'] = '°C'
            sensor['identifier'] = obs['source_id']
            sensor['value'] = obs['value']
            if obs['source_id'] in parameter_field:
                parameters = parameter_field[obs['source_id']]
                parameter = sensor['entity']
                if parameters and (parameter in parameters):
                    device_class = parameters[parameter]
                    sensor['device_class'] = device_class
            else:
                source_id = obs['source_id']
                logging.warning(f'source_id {source_id} not in definition, device_class not mapped')
            # sensor[obs['parameter']+'_QC'] = obs['qualityCodes']

            data_points.append((time_str, sensor, metadata_dp))

    # temporary fix to handle wsense nodes with 2 data points differing only in milliseconds
    # if len(data_points) == 2:
    #
    #     t0 = datetime.datetime.fromisoformat(data_points[0][0]).strftime('%Y-%m-%dT%H:%M:%S+%z')
    #     t1 = datetime.datetime.fromisoformat(data_points[1][0]).strftime('%Y-%m-%dT%H:%M:%S+%z')
    #
    #     if t0 == t1:
    #         data_points[0] = (data_points[0][0],
    #                           [data_points[0][1][i] if data_points[0][1][i] is not None else data_points[1][1][i]
    #                            for i in range(CHANNEL_FIELD_MAX)])
    #
    #         data_points.pop()

    return data_points


def get_time(ts_data_str):
    ts_data = json.loads(ts_data_str)
    data = ts_data['data'][0]
    time_str = data['time']  # TODO: should validate that it is iso format
    return time_str
