import os
import zipfile
import shutil
import pandas as pd

import glob
import time
from send_request.GeoLabAPI import GeoLabAPI
from send_request.pgDB import pgDB


path = "../sent/"
API = GeoLabAPI()
DB = pgDB("localhost", "mydata", "postgres", "postgreut99")
tableName = API.get_table_name(12345678)

def get_file_name_toint(file):
    filename_w_ext = os.path.basename(file)
    filename, file_extension = os.path.splitext(filename_w_ext)
    return int(filename)

def zip_move(name):
    try:
        import zlib
        mode= zipfile.ZIP_DEFLATED
    except:
        mode= zipfile.ZIP_STORED
    try:
        name = int(name[:-4])
    except Exception as ex:
        print(">> move_and_zip / error:  Can not convert name file to integer.\n", ex)
    try:
        zipfile.ZipFile(str(name) + ".zip", 'w', mode).write(str(name) + ".txt")
        shutil.move(str(name) + ".zip", path + str(name) + ".zip")
        os.remove(str(name) + ".txt")
    except OSError:
        os.remove(str(name) + ".zip")
        print(">> move_and_zip / error:  Can not create zip file or move or remove %s file"% (str(name) +'.txt')) 


if os.path.isdir(path):
    print(">> move_and_zip / info:  Directory has exist")
else:
    try:
        os.mkdir(path)
    except OSError:
        print (">> move_and_zip / error:  Creation of the directory %s failed" % path)
    else:
        print (">> move_and_zip / info:  Successfully created the directory %s " % path)



Loop = True
temp_size = 0
while Loop:
    try:
        files = glob.glob("../Obs/*.txt")
        if len(files) != 0:
            name = max(list(map(get_file_name_toint, files)))
            current_file = str(name) + ".txt"
            for file in files:
                if file == current_file: continue

                f = pd.read_csv(file, sep=' ', header=["T", "AX", "AY", "AZ", "TEMP"])
                for counter in range(3):
                    try:
                        query = ""
                        for inx, data in f.iterrows():
                            query += "insert into data(t, a_x, a_y, a_z, temp) values ({},{},{},{},{});\n".format(data["T"], data["AX"], data["AY"], data["AZ"], data["TEMP"])

                        DB.setQuery(query)
                    except Exception as ex:
                        print(">> move_and_zip / error:  %d. The %s don't saved on local database.\n" % (counter + 1, file) ,ex)
                        continue
                    else:
                        print(">> move_and_zip / info:  The %s saved on local database." % file)
                        zip_move(file)
                        break
            
            data_count = 0
            try:
                dontSentData = DB.getQuery("select * from data where not is_sent")
                API.send_data(tableName, dontSentData)
            except Exception as ex:
                print(">> move_and_zip / error:  send data faild.\n" ,ex)
            else:
                print(">> move_and_zip / info:  %d from datas sent." % data_count)
            
            time.sleep(5)
        else:
            print(">> move_and_zip / info:  No file in this directory ")
            time.sleep(1)
    except Exception as ex:
        print(">> move_and_zip / error:  read files faild\n" ,ex)