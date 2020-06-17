endl = '\n'

def GetGeoJsonStations(stations):
    features = ""
    for i in range(len(stations)):
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
        }},""".format(stations[i][0],
                stations[i][1],
                '',
                stations[i][2],
                stations[i][3],
                'Active' if stations[i][4] == True else 'Inactive',
                stations[i][5],
                '' if stations[i][6] == None else stations[i][6],
                stations[i][7],
                stations[i][8])
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