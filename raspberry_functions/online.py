#!/usr/bin/python3

import glob
import os
import time
from send_request.GeoLabAPI import GeoLabAPI
from send_request.log import log, messageType

obs_path = "../Obs/"
log_path = "./Log/online.txt"

API = GeoLabAPI()
log = log(log_path)

def get_table_name(id):
    while True:
        try:
            return API.get_table_name(id)
        except Exception as ex:
            log.log("get table name faild", messageType.ERROR)
            time.sleep(0.5)
            continue

def get_file_name_toint(file):
    filename_w_ext = os.path.basename(file)
    filename, file_extension = os.path.splitext(filename_w_ext)
    return int(filename)

tableName = get_table_name(12345678)

Loop = True
temp_size = 0
while Loop:
    try:
        files = glob.glob(obs_path + "*.txt")
        if len(files) != 0:
            name = max(list(map(get_file_name_toint, files)))
            file_name = obs_path + str(name) + ".txt"
            size = os.stat(file_name).st_size
            if size > temp_size:
                try:
                    API.send_health_status(tableName, 1)
                    log.log("health code (1) sent. The file size has changed", messageType.INFO)
                except Exception as ex:
                    log.log("health code (1) don't sent. The file size has changed\n%s" % ex, messageType.ERROR)
            else:
                try:
                    API.send_health_status(table_name, 2)
                    log.log("health code (2) sent. The file size has not changed", messageType.INFO)
                except Exception as ex:
                    log.log("health code (2) don't sent. The file size has not changed\n%s" % ex, messageType.ERROR)
            temp_size = size
            time.sleep(5)
        else:
            log.log("No file in this directory", messageType.INFO)
            time.sleep(1)
    except Exception as ex:
        log.log("read files faild\n%s" % ex, messageType.ERROR)
