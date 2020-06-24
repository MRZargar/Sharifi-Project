import glob
import os
import time
def name_to_number(name):
    return int(name[:-4])

files = glob.glob("*.txt")
print(files)
name = max(list(map(name_to_number, files)))
file_name = str(name) + ".txt"

temp_size = 0
while True:
    size = os.stat(file_name).st_size
    if size > temp_size:
        print("the file size has changed")
    else:
        print("the file size has not changed")
    temp_size = size
    time.sleep(5)
