import glob
import os
import time
def name_to_number(name):
    return int(name[:-4])

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
                print("the file size has changed")
            else:
                print("the file size has not changed")
            temp_size = size
            time.sleep(5)
        else:
            print("No file in this directory ")
            time.sleep(1)
    except Exception as ex:
        print(ex)
