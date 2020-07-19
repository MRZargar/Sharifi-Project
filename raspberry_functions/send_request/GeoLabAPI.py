import json as JSON
import numpy as np
import requests
from typing import Text

class GeoLabAPI:
    base_url: str = "http://84.241.62.31:8080/api/Data/"

    def get_table_name(self, raspberryId: int) -> Text:
        url = self.base_url + "{}/313".format(raspberryId)
        
        r = requests.get(url, verify=False)

        if r.status_code != 200:
            raise Exception(r.status_code)

        return r.text
    
    def send_raspberry_id(self, raspberryId: int) -> None:
        url = self.base_url + "{}/313".format(raspberryId)

        r = requests.post(url, verify=False)

        if r.status_code not in range(200,300):
            raise Exception(r.status_code)
    
    def send_data(self, table_name: str, datas) -> None:
        url = self.base_url + "{}".format(table_name)

        json = "["
        for inx, data in datas.iterrows():
            json = json + "[{},{},{},{},{},{}],".format(data.week, data.t, data.a_x, data.a_y, data.a_z, 'null' if np.isnan(data.temp) else data.temp)

        json = json[:-1] + "]" 

        json = JSON.loads(json)

        r = requests.post(url, json=json, verify=False)

        if r.status_code not in range(200,300):
            raise Exception(r.status_code)
    
    def send_health_status(self, table_name: str, health_code: int):
        url = self.base_url + "{}".format(table_name)

        json = "{{ \"healthCode\" : {} }}".format(health_code)
        json = JSON.loads(json)

        r = requests.put(url, json=json, verify=False)

        if r.status_code not in range(200,300):
            raise Exception(r.status_code)