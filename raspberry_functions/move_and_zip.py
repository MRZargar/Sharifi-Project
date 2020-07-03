import os
import zipfile
import shutil
import pandas as pd

import glob
import time
from send_request.GeoLabAPI import GeoLabAPI
from send_request.pgDB import pgDB

obs_path = "../Obs/"
sent_path = "../sent/"
one_min_data_count = 60*100
API = GeoLabAPI()
DB = pgDB("localhost", "mydata", "postgres", "postgreADXL99")
tableName = API.get_table_name(12345678)

def get_file_name_toint(file):
    return int(get_file_name(file))

def get_file_name(file):
    filename_w_ext = os.path.basename(file)
    filename, file_extension = os.path.splitext(filename_w_ext)
    return filename

def zip_move(name):
    try:
        import zlib
        mode= zipfile.ZIP_DEFLATED
    except:
        mode= zipfile.ZIP_STORED
    
    name = get_file_name(name)

    try:
        zipfile.ZipFile(sent_path + name + ".zip", 'w', mode).write(obs_path + name + ".txt")
        os.remove(obs_path + name + ".txt")
    except OSError:
        os.remove(str(name) + ".zip")
        print(">> move_and_zip / error:  Can not create zip file or move or remove %s file"% (str(name) +'.txt')) 
    else:
        print(">> move_and_zip / info:  created and moved zip file and then remove %s file"% (str(name) +'.txt')) 


def create_sent_directory(path):
    if os.path.isdir(path):
        print(">> move_and_zip / info:  Directory has exist")
    else:
        try:
            os.mkdir(path)
        except OSError:
            print (">> move_and_zip / error:  Creation of the directory %s failed" % path)
        else:
            print (">> move_and_zip / info:  Successfully created the directory %s " % path)

def import_to_db(query, cnt):
    for i in range(3):
        try:
            DB.setQuery(query)
        except Exception as ex:
            print(">> move_and_zip / error: %d. The %d row from %s don't saved on local database.\n" % (i+1, cnt, file_name), ex)
            # ------------------------------------------
        else:
            print(">> move_and_zip / info: %d. The %d row from %s saved on local database." % (i+1, cnt, file_name))
            break

def save_data_on_db(file_name):
    query = ""
    temp_cnt = 0
    with open(file_name) as fp:
        for cnt, data in enumerate(fp):
            query += "insert into data(t, a_x, a_y, a_z, temp) values ({});\n".format(data.replace(' ', ','))
            
            if cnt % one_min_data_count == 0:
                import_to_db(query, cnt - temp_cnt)
                temp_cnt = cnt
                query = ""
        
        if query != "":
            import_to_db(query, cnt - temp_cnt)

def save_data(files):
    if len(files) == 0:
        return
        
    name = max(list(map(get_file_name_toint, files)))
    current_file = obs_path + str(name) + ".txt"
    for file in files:
        if file == current_file: continue

        try:
            save_data_on_db(file)
        except Exception as ex:
            print(">> move_and_zip / error:  Can't read The %s.\n" % file ,ex)
        else:
            print(">> move_and_zip / info:  The %s saved on local database." % file)
            zip_move(file)            

def submit_data(datas):
    query = "update data set is_sent = TRUE where "

    for inx, data in datas.iterrows():
        query += "t = " + str(data.t) + " OR "

    query += query[:-3] + ";"

    for i in range(3):
        try:
            DB.setQuery(query)
        except Exception as ex:
            print(">> move_and_zip / error: %d. Faild for submit %d row.\n" % (i+1, len(datas)), ex)
            # if i == 2:
            #     pass
        else:
            print(">> move_and_zip / error: %d. submited %d row.\n" % (i+1, len(datas)))
            break

def send_data(data):
    for i in range(3):
        try:                
            API.send_data(tableName, data)
            submit_data(data)
        except Exception as ex:
            print(">> move_and_zip / error: %d. %d from datas don't sent." % (i+1, len(data)))
        else:
            print(">> move_and_zip / info: %d. %d from datas sent." % (i+1, len(data)))
            break

# --------------------------------------------------------------------------

create_sent_directory(sent_path)

while True:
    files = glob.glob(obs_path + "*.txt")

    try:
        save_data(files)
    except Exception as ex:
        print(">> move_and_zip / error:  read files faild\n" ,ex)

    while True:
        dontSentData = DB.getQuery("select * from data where not is_sent limit " + str(one_min_data_count))
        if len(dontSentData) == 0 : break

        send_data(dontSentData)
    
    time.sleep(5)