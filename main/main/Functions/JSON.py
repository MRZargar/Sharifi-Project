endl = '\n'
import sys
import datetime
sys.path.append("...")
from stations.models import Deactivate
def GetGeoJsonStations(stations, *args):
    features = ""
    if args == ('user',):
        for station in stations:
            db_time = datetime.datetime(station.health_time.year, station.health_time.month, station.health_time.day, station.health_time.hour, station.health_time.minute, station.health_time.second)      
            time = datetime.datetime.now() - db_time
            if time.total_seconds() > 10:
                helath = 2
            else:
                helath = station.helath
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
                    'Health': '{9}'
                }},
                'geometry': {{
                'type': 'Point',
                'coordinates': [{7}, {8}]
                }}
            }},""".format(station.id,
                    station.station_name,
                    station.sensor_type,
                    station.address,
                    'Active' if station.status == True else 'Inactive',
                    station.date,
                    '' if station.status == True else Deactivate.objects.get(station_name_id = station.pk),
                    station.longitude,
                    station.latitude,
                    helath)
        features = features[:-1]
    else:
        for station in stations: 
            db_time = datetime.datetime(station.health_time.year, station.health_time.month, station.health_time.day, station.health_time.hour, station.health_time.minute, station.health_time.second)      
            time = datetime.datetime.now() - db_time
            if time.total_seconds() > 10:
                helath = 2
            else:
                helath = station.helath

            print(helath)
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
                    'Latitude': '{9}',
                    'Health' : {10}
                }},
                'geometry': {{
                'type': 'Point',
                'coordinates': [{8}, {9}]
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
                    station.latitude,
                    helath)
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