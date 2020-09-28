from datetime import datetime, timedelta
from gwpy.time import tconvert, to_gps
import os
import shutil 
import zipfile
import requests
from download.models import DownloadLink
from stations.models import Setup
from django.conf import settings

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def write_to_text(file_name, data):
    data = data[2:-2].split('],[')
    with open(file_name, 'w') as fp:
        for row in data:
            row = row.split(",")[1:]
            fp.write('%.3f ' % float(row[0]))
            fp.write('%.4f ' % float(row[1]))
            fp.write('%.4f ' % float(row[2]))
            fp.write('%.4f ' % float(row[3]))
            fp.write('%.2f\n' % float(row[4]))
        fp.close()


def get_data(table_name, from_week, from_second, to_week, to_second):
    url = settings.GEOLABAPI_HOST + ':' + settings.GEOLABAPI_PORT + '/api/Data/{}?fromWeek={}&fromT={}&toWeek={}&toT={}'.format(table_name, from_week, from_second, to_week, to_second)
    r = requests.get(url, verify=False)
    if r.status_code not in range(200,300):
        raise Exception(r.status_code)
    return r.text



# Convet time to gps week and seconds
def cleander_to_gps(year, month, day, hour, minute, second):
    time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    all_seconds = to_gps(time) - 18
    week = int(all_seconds/604800)
    second = all_seconds % 604800 
    return (week, second)



def create_download_link():
    download_links = DownloadLink.objects.all().order_by('request_date')
    for download in download_links:
        if download.status:
            pass
        else:
            download_path = '/home/geolab/site/main/media/download_link'
            number_of_downloaded = download.number
            stations_id = download.stations_id
            from_date = download.from_date
            to_date = download.to_date
            start_hour = download.start_hour
            end_hour = download.end_hour
            from_date = from_date.split("/")
            to_date = to_date.split("/")
            from_time = (datetime(int(from_date[0]), int(from_date[1]), int(from_date[2]))) 
            to_time = (datetime(int(to_date[0]), int(to_date[1]), int(to_date[2]))) 
            delta = to_time - from_time
            stations = []
            station_id = []
            main_file_name = ""
            all_stations_id = stations_id[1:].split("-")
            for station in all_stations_id:
                main_file_name += station
            main_file_name += from_date[0] + from_date[1] + from_date[2]  + to_date[0] + to_date[1] + to_date[2]
            os.chdir(download_path)
            if not os.path.exists(str(number_of_downloaded)):
                os.mkdir(str(number_of_downloaded))
            os.chdir(str(number_of_downloaded))
            main_dir = main_file_name
            if not os.path.exists(main_dir):
                os.mkdir(main_dir)
            os.chdir(main_dir) 
            for i in range(len(all_stations_id)):
                station_char = all_stations_id[i]
                station_dir = str(station_char)
                station = Setup.objects.get(station_id=station_char)
                station_table = station.table_name
                if not os.path.exists(station_dir):
                    os.mkdir(station_dir)
                for day in range(delta.days + 1):
                    date = from_time + timedelta(days=day)       
                    for hour in range(start_hour, end_hour+1):
                        from_week, from_second = cleander_to_gps(date.strftime("%Y"), date.strftime("%m"), date.strftime("%d"), hour, 0, 0)
                        to_week, to_second = from_week, from_second + 3600
                        data = get_data(station_table, from_week, from_second, to_week, to_second)
                        if len(data) == 2:
                            pass
                        else:
                            if len(str(hour)) == 2:
                                hour = str(hour)
                            else:
                                hour = '0' + str(hour)
                            file_name = station_dir + "/" +  str(station_char) + str(date.strftime("%Y")) + date.strftime("%m") + date.strftime("%d") + hour +"0000" + ".txt"
                            write_to_text(file_name, data)
            os.chdir(download_path + '/' + str(number_of_downloaded))
            zipf = zipfile.ZipFile(main_file_name + '.zip', 'w', zipfile.ZIP_DEFLATED)
            zipdir(main_dir , zipf)
            zipf.close()
            if os.path.exists(main_dir):
                shutil.rmtree(main_dir)
            download_link_user = "/media/download_link/" + str(number_of_downloaded) + '/' + main_file_name + '.zip'
            download_size = round(os.path.getsize(str(main_file_name) + '.zip')/(1000*1000), 1)
            download.download_link = download_link_user
            download.size = download_size
            download.status = True
            download.save()



def delete_download_link():
    UTC_time = timedelta(hours=4, minutes=30, seconds=0)
    download_link = DownloadLink.objects.all().order_by('request_date')
    for download in download_link:
        db_time = datetime(download.request_date.year, download.request_date.month, download.request_date.day, download.request_date.hour, download.request_date.minute, download.request_date.second)
        db_time += UTC_time
        delta_time = abs((datetime.now() - db_time).days)
        if delta_time > 7 and download.status == True and download.dic_delete == False:
            download_path = '/home/geolab/site/main/media/download_link'
            os.chdir(download_path)
            shutil.rmtree(str(download.number))
            download.dic_delete = True
            download.save()