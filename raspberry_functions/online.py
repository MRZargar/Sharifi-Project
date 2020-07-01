import glob
import os
import time
from send_request.GeoLabAPI import GeoLabAPI

def name_to_number(name):
    return int(name[:-4])

API = GeoLabAPI()

tableName = API.get_table_name(12345678)

Loop = True
temp_size = 0
while Loop:
    try:
        files = glob.glob("*.txt")
        if len(files) != 0:
            name = max(list(map(name_to_number, files)))
            file_name = str(name) + ".txt"
            size = os.stat(file_name).st_size
            if size > temp_size:
                try:
                    API.send_health_status(table_name, 1)
                except Exception as ex:
                    print(">> online / error:  health code (1) don't sent. The file size has changed\n", ex)
                print(">> online / info:  health code (1) sent. The file size has changed")
            else:
                try:
                    API.send_health_status(table_name, 2)
                except Exception as ex:
                    print(">> online / error:  health code (2) don't sent. The file size has not changed\n", ex)
                print(">> online / info:  health code (2) sent. The file size has not changed")
            temp_size = size
            time.sleep(5)
        else:
            print(">> online / info:  No file in this directory ")
            time.sleep(1)
    except Exception as ex:
        print(">> online / error:  read files faild\n" ,ex)
