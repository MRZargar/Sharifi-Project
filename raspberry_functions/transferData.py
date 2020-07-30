#!/usr/bin/python3

import os
import zipfile
import shutil
import pandas as pd
import psycopg2
import glob
import time
import multiprocessing
from send_request.GeoLabAPI import GeoLabAPI
from send_request.pgDB import pgDB
from send_request.log import log, messageType

obs_path = "../Obs/"
sent_path = "../sent/"
log_path = "./Log/transferData.txt"
DB = pgDB("localhost", "mydata", "postgres", "postgreADXL99")

one_min_to_sec = 60
one_min_data_count = one_min_to_sec * 100
API = GeoLabAPI()
log = log(log_path)

def get_table_name(id):
    while True:
        try:
            return API.get_table_name(id)
        except Exception as ex:
            log.log("(E1) get table name faild", messageType.ERROR)
            time.sleep(0.5)
            continue

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
        log.log("(E7) Can not create zip file or move or remove [%s] file" % (str(name) +'.txt'), messageType.ERROR)
    else:
        log.log("created and moved zip file and then remove [%s] file" % (str(name) +'.txt'), messageType.INFO)


def create_sent_directory(path):
    if os.path.isdir(path):
        log.log("Directory has exist", messageType.INFO)
    else:
        try:
            os.mkdir(path)
        except OSError:
            log.log("(E2) Creation of the directory [%s] failed" % path, messageType.ERROR)
        else:
            log.log("Successfully created the directory [%s]" % path, messageType.INFO)

def import_to_db(query, cnt, file_name):
    for i in range(3):
        try:
            DB.setQuery(query)
            break
        except Exception as ex:
            queries = query.split(';')
            for q in queries:
                try:
                    DB.setQuery(q)
                except psycopg2.IntegrityError:
                    continue
                except Exception as ex:
                    log.log("(E6) {{ %s }} from [%s] file don't saved.\n%s" % (q, file_name, ex), messageType.ERROR)

def save_data_on_db(file_name):
    query = ""
    temp_cnt = 0
    week = str(get_file_name_toint(file_name))[:-6]
    with open(file_name) as fp:
        for cnt, data in enumerate(fp):
            query += "insert into data values ({}, {}, false);\n".format(week, data.replace(' ', ','))
            
            if cnt % one_min_data_count == 0:
                import_to_db(query, cnt - temp_cnt, file_name)
                temp_cnt = cnt
                query = ""
        
        if query != "":
            import_to_db(query, cnt - temp_cnt, file_name)

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
            log.log("(E4) Can't read The [%s].\n%s" % (file, ex), messageType.ERROR)
        else:
            log.log("The [%s] saved on local database" % file, messageType.INFO)
            zip_move(file)            

def submit_data(datas):
    query = ""
    for _, data in datas.iterrows():
        query += "update data set is_sent = TRUE where week = {} AND t = {};\n".format(data.week, data.t)

    for i in range(3):
        try:
            DB.setQuery(query)
        except Exception as ex:
            log.log("(E9) %d. Faild for submit %d row.\n%s" % (i+1, len(datas), ex), messageType.ERROR)
            if i == 2:
                log.log("(E10)",messageType.ERROR)
        else:
            log.log("%d. submited %d row" % (i+1, len(datas)), messageType.INFO)
            break

def send_data(data):
    for i in range(3):
        try:   
            API.send_data(tableName, data)
            log.log("%d. %d from datas sent" % (i+1, len(data)), messageType.INFO)
            submit_data(data)
            break
        except Exception as ex:
            log.log("(E8) %d. %d from datas don't sent.\n%s" % (i+1, len(data), ex), messageType.ERROR)
            

# --------------------------------------------------------------------------
tableName = get_table_name(12345678)

create_sent_directory(sent_path)

while True:
    files = glob.glob(obs_path + "*.txt")

    try:
        # save_data(files)
    except Exception as ex:
        log.log("(E3) read files faild.\n%s" % ex, messageType.ERROR)

    t1 = time.time()
    dt = 0
    # ???
    while dt < 3 * one_min_to_sec: 
        dontSentData = DB.getQuery("select * from data where not is_sent order by week asc, t asc limit " + str(2 * one_min_data_count))
        if len(dontSentData) == 0 : break

        count = len(dontSentData)
        step = count / 3
        threads = []
        for i in range(3):
            start = i * step
            end = start + step
            thread = multiprocessing.Process(target=send_data, args=(dontSentData[start:end]))
            threads.append(thread)

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
        
        t2 = time.time()
        dt = t2 - t1

    
    time.sleep(5)