from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from stations.models import Setup, Access
from datetime import datetime, timedelta
from gwpy.time import tconvert, to_gps
from .models import DownloadLink
import requests
from django.shortcuts import render


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
        for station in stations:
            station_list.append(station.station_id)
        return JsonResponse({'stations_list': station_list}, status=200)

    elif request.method == "GET" and request.GET['method'] == "download":
        number_of_downloaded = DownloadLink.objects.all().count()
        stations_id = request.GET.getlist('StaionsId[]')
        all_stations_id = ""
        for station_id in stations_id:
            all_stations_id += "-" + station_id
        start_hour = request.GET['StartHour']
        end_hour = request.GET['EndHour']
        from_date_main = request.GET['StartTime']
        to_date_main = request.GET['EndTime']
        from_date = from_date_main.split("/")
        to_date = to_date_main.split("/")
        from_time = (datetime(int(from_date[0]), int(from_date[1]), int(from_date[2]))) 
        to_time = (datetime(int(to_date[0]), int(to_date[1]), int(to_date[2]))) 
        if (to_time - from_time).total_seconds() < 0 or int(end_hour) < int(start_hour):
            return JsonResponse({}, status=400)
        else:
            DownloadLink.objects.create(user=request.user,
                                        stations_id=all_stations_id,
                                        from_date=from_date_main,
                                        to_date=to_date_main,
                                        start_hour=start_hour,
                                        end_hour=end_hour,
                                        number=number_of_downloaded,   
            )
            return JsonResponse({}, status=200)


@login_required(login_url='signpage')
def requests_list(request, pk):
    download_links = DownloadLink.objects.filter(user=request.user).order_by('request_date').reverse()
    return render(request, 'download_list.html', {'download_links':download_links})




