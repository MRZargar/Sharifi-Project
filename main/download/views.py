from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from stations.models import Setup, Access
from datetime import datetime, timedelta
from gwpy.time import tconvert, to_gps
import os
import shutil 
import zipfile
from .models import DownloadLink
import requests
def zipdir(path, ziph):
    # ziph is zipfile handle
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
    url = 'http://84.241.62.31:8080/api/Data/{}?fromWeek={}&fromT={}&toWeek={}&toT={}'.format(table_name, from_week, from_second, to_week, to_second)
    try:
        r = requests.get(url, verify=False)
    except SocketError as e:
        pass
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


def gps_to_cleander(week, second):
    all_seconds = week * 604800 + second + 18
    return tconvert(all_seconds)



@login_required(login_url='signpage')
def download(request, pk):
    if request.method == "GET" and request.GET['method'] == "give station name":
        obj = request.user
        if obj.userType == "is_admin":
            stations = Setup.objects.all().order_by('date').reverse()
        else:
            station_access = Access.objects.filter(user_id = obj.id)
            user_access = []
            for station_q in station_access:
                user_access.append(station_q.station_id)
            stations = Setup.objects.filter(id__in = user_access).order_by('date').reverse()
        station_list = []
        station_names = []
        for station in stations:
            station_list.append(station.for_character_id)
            station_names.append(station.station_name)
        return JsonResponse({'stations_list': station_list, 'station_name':station_names}, status=200)

    elif request.method == "GET" and request.GET['method'] == "download":
        number_of_downloaded = DownloadLink.objects.all().count()
        download_path = '/home/geolab/site/main/media/download_link'
        stations_character_id = request.GET.getlist('StaionsName[]')
        hours = request.GET.getlist('Hours[]')
        from_date = request.GET['StartTime']
        to_date = request.GET['EndTime']
        from_date = from_date.split("/")
        to_date = to_date.split("/")
        from_time = (datetime(int(from_date[0]), int(from_date[1]), int(from_date[2]))) 
        to_time = (datetime(int(to_date[0]), int(to_date[1]), int(to_date[2]))) 
        if (to_time - from_time).total_seconds() < 0:
            return JsonResponse({}, status=400)
        else:
            delta = to_time - from_time
            stations = []
            station_char_id = []
            main_file_name = ""
            for station in stations_character_id:
                station_db = Setup.objects.get(for_character_id=station)
                station_char_id.append(station_db.for_character_id)
                stations.append(station_db.table_name)
                main_file_name += station_db.for_character_id 
            main_file_name += from_date[0] + from_date[1] + from_date[2]  + to_date[0] + to_date[1] + to_date[2]
            os.chdir(download_path)
            if not os.path.exists(str(number_of_downloaded)):
                os.mkdir(str(number_of_downloaded))
            os.chdir(str(number_of_downloaded))
            main_dir = main_file_name
            if not os.path.exists(main_dir):
                os.mkdir(main_dir)
            os.chdir(main_dir)
            for i in range(len(stations)):
                station_table = stations[i]
                station_char = station_char_id[i]
                station_dir = str(station_char)
                if not os.path.exists(station_dir):
                    os.mkdir(station_dir)
                for day in range(delta.days + 1):
                    date = from_time + timedelta(days=day)
                    for hour in hours:
                        from_week, from_second = cleander_to_gps(date.strftime("%Y"), date.strftime("%m"), date.strftime("%d"), (int(hour)-1), 0, 0)
                        to_week, to_second = from_week, from_second + 3600
                        data = get_data(station_table, from_week, from_second, to_week, to_second)
                        if len(data) == 2:
                            pass
                        else:
                            if len(str(int(hour)-1)) == 2:
                                hour = str(int(hour)-1)
                            else:
                                hour = '0' + str(int(hour)-1)
                                
                            file_name = station_dir + "/" +  str(station_char) + str(from_week) + str(date.strftime("%Y")) + date.strftime("%m") + date.strftime("%d") + hour +"0000" + ".txt"
                            write_to_text(file_name, data)
                zipf = zipfile.ZipFile(station_dir + '.zip', 'w', zipfile.ZIP_DEFLATED)
                zipdir(station_dir + '/', zipf)
                zipf.close()
                shutil.rmtree(station_dir)
            os.chdir(download_path + '/' + str(number_of_downloaded))
            zipf = zipfile.ZipFile(main_file_name + '.zip', 'w', zipfile.ZIP_DEFLATED)
            zipdir(main_dir , zipf)
            zipf.close()
            shutil.rmtree(main_dir)
            download_link_user = "/media/download_link/" + str(number_of_downloaded) + '/' + main_file_name + '.zip'
            download_size = round(os.path.getsize(str(main_file_name) + '.zip')/(1000*1000), 1)
            DownloadLink.objects.create(user=request.user, download_link=download_link_user, size=download_size)
            return JsonResponse({'link':download_link_user}, status=200)