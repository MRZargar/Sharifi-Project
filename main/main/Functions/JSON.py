endl = '\n'
import sys
sys.path.append("...")
from stations.models import Deactivate
def GetGeoJsonStations(stations, *args):
    features = ""
    if args == ('user',):
        for station in stations:
            features += """
            {{
                'type': 'Feature',
                'properties': {{
                    'ID' : '{0}',
                    'Name': '{1}',
                    'Sensor Type': '{2}',
                    'Address': '{3}',
                    'Status': '{4}',
                    'Start Time': '{5}',
                    'End Time': '{6}',
                    'Longitude': '{7}',
                    'Latitude': '{8}'
                }},
                'geometry': {{
                'type': 'Point',
                'coordinates': [{8}, {7}]
                }}
            }},""".format(station.id,
                    station.station_name,
                    station.sensor_type,
                    station.address,
                    'Active' if station.status == True else 'Inactive',
                    station.date,
                    '' if station.status == True else Deactivate.objects.get(station_name_id = station.pk),
                    station.longitude,
                    station.latitude)
        features = features[:-1]
    else:
        for station in stations:
            features += """
            {{
                'type': 'Feature',
                'properties': {{
                    'ID': '{0}',
                    'Name': '{1}',
                    'Operator': '{2}',
                    'Sensor Type': '{3}',
                    'Address': '{4}',
                    'Status': '{5}',
                    'Start Time': '{6}',
                    'End Time': '{7}',
                    'Longitude': '{8}',
                    'Latitude': '{9}'
                }},
                'geometry': {{
                'type': 'Point',
                'coordinates': [{9}, {8}]
                }}
            }},""".format(station.id,
                    station.station_name,
                    station.operator.username,
                    station.sensor_type,
                    station.address,
                    'Active' if station.status == True else 'Inactive',
                    station.date,
                    '' if station.status == True else Deactivate.objects.get(station_name_id = station.pk),
                    station.longitude,
                    station.latitude)
        features = features[:-1]

    geojson = """{
        'type': 'FeatureCollection', 
        'crs': {
            'type': 'name',
            'properties': {
            'name': 'EPSG:4326'
            }
        },
        'features': [
            """ + features + "]}"    
    
    return geojson

def GetPoltData(datas):
    ax = '`t, value' + endl
    ay = '`t, value' + endl
    az = '`t, value' + endl
    
    # for data in datas:
        # ax += data[t] + ', ' + data[ax] + endl
        # ay += data[t] + ', ' + data[ay] + endl
        # az += data[t] + ', ' + data[az] + endl
    
    ax += '`'
    ay += '`'
    az += '`'

    return ax, ay, az

def GetHistData(datas):
    result = '`Hours, Value' + endl
    
    # for i in range(len(datas)):
        # result += str(i+1) + ', ' + datas[i] + endl
    
    result += '`'

    return result