from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import os
from django.contrib.auth import get_user_model
from users.models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib import auth
from django.http import JsonResponse
import json
from .Functions import JSON
from stations.models import Setup, Access, Deactivate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from message.models import Message
from datetime import datetime, timedelta
from gwpy.time import tconvert, to_gps
import requests
from django.conf import settings
User = get_user_model()

def update_hist(table_name, gps_week, second):
    url = settings.GEOLABAPI_HOST + ':' + settings.GEOLABAPI_PORT + '/api/Data/Histogram/{}?week={}&t={}'.format(table_name, gps_week, second)
    print("-----------------------------------------------")
    print(url)
    print("-----------------------------------------------")
    r = requests.get(url, verify=False)
    if r.status_code not in range(200,300):
        raise Exception(r.status_code)
    return [float(i) for i in r.text[1:-1].split(',')]

def get_data(table_name, from_week, from_second, to_week, to_second):
    url = settings.GEOLABAPI_HOST + ':' + settings.GEOLABAPI_PORT + '/api/Data/{}?fromWeek={}&fromT={}&toWeek={}&toT={}'.format(table_name, from_week, from_second, to_week, to_second)
    r = requests.get(url, verify=False)
    if r.status_code not in range(200,300):
        raise Exception(r.status_code)
    return r.text

def preparation_plot_data(data):
    data = data[2:-2].split('],[')
    ax, ay, az, temp = [], [], [], []
    for row in data:
        ax.append([float(row.split(',')[1]), float(row.split(',')[2])])
        ay.append([float(row.split(',')[1]), float(row.split(',')[3])])
        az.append([float(row.split(',')[1]), float(row.split(',')[4])])
        temp.append([float(row.split(',')[1]), float(row.split(',')[5])])
    ax_str = '`t, value\n'
    ay_str = '`t, value\n'
    az_str = '`t, value\n'
    temp_str = '`t, value\n'
    for i in range(len(ax)):
        ax_str += str(ax[i][0]) + ',' + str(ax[i][1]) + '\n'
        ay_str += str(ay[i][0]) + ',' + str(ay[i][1]) + '\n'
        az_str += str(az[i][0]) + ',' + str(az[i][1]) + '\n'
        temp_str += str(temp[i][0]) + ',' + str(temp[i][1]) + '\n'
    ax_str += '`'
    ay_str += '`'
    az_str += '`'
    temp_str += '`'
    return ax_str, ay_str, az_str, temp_str


# Convet time to gps week and seconds
def cleander_to_gps(year, month, day, hour, minute, second):
    time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    all_seconds = to_gps(time) - 18
    week = int(all_seconds/604800)
    second = all_seconds % 604800 
    return (week, second)


def home_page(request):
    return render(request, "geolab.html")

def signpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.email_confirmed == True and user.admin_confirmed == True:
            pk = user.pk
            request.session['username'] = username
            if user.userType == 'is_user':
                auth.login(request, user)
                return redirect("map")
            elif user.userType == 'is_operator':
                    auth.login(request, user)
                    return redirect("map")
            elif user.userType == 'is_admin':
                    auth.login(request, user)
                    return redirect("map")
        else:
            messages.error(request, "Wrong username or password")
            return redirect('signpage')

    else:
        return render(request, 'Signin.html', {})


@login_required(login_url='signpage')
def UserProfile(request, pk):
    obj = request.user
    if obj.userType != 'is_user':
        raise PermissionDenied
    else:
        return render(request, 'UserHome.html')


@login_required(login_url='signpage')
def OperatorProfile(request, pk):
    obj = request.user
    if obj.userType != 'is_operator':
        raise PermissionDenied
    else:
        return render(request, 'OperatorHome.html')

@login_required(login_url='signpage')
def AdminProfile(request, pk):
    obj = request.user
    if obj.userType != 'is_admin':
        raise PermissionDenied
    else:
        return render(request, 'AdminHome.html')

@login_required(login_url='signpage')
def inbox_message_view(request, pk):
    user_inbox = Message.objects.filter(reciver = request.user)
    number_of_inbox = user_inbox.count()
    return JsonResponse({'count':number_of_inbox}, status=200)


def signout(request):
    auth.logout(request)
    return render(request,'Signin.html')

@login_required(login_url='signpage')
def plot_update(request):
        station_id = request.GET['StationId']
        station = Setup.objects.get(station_id=station_id)
        station_table = station.table_name
        date = request.GET['Date']
        to_date = int(request.GET['Hour'])
        from_date = to_date
        date = date.split("/")
        from_week, from_second = cleander_to_gps(date[0], date[1], date[2], from_date, 0, 0)
        to_week, to_second = from_week ,from_second + 3600
        data = get_data(station_table,from_week, from_second, to_week, to_second)
        xPlotData, yPlotData ,zPlotData, tempPlotData = preparation_plot_data(data)
        return JsonResponse({'xPlotData':xPlotData, 'yPlotData':yPlotData, 'zPlotData':zPlotData, 'tempPlotData':tempPlotData}, status=200)

@login_required(login_url='signpage')
def histogram_update(request):
    if request.method == "GET":
        station_id = request.GET['StationId']
        from_date = request.GET['Date']
        station = Setup.objects.get(station_id=station_id)
        station_table = station.table_name
        from_date = from_date.split("/")
        gps_week, second = cleander_to_gps(int(from_date[0]), int(from_date[1]), int(from_date[2]), 0, 0, 0)
        hist_data = update_hist(station_table, gps_week, second)
        return JsonResponse({'hist_data':hist_data}, status=200)
    else:
        return JsonResponse({}, status=400)


@login_required(login_url='signpage')
def plot(request, stationID):

    #user access for tree view  
    obj = request.user
    if obj.userType == 'is_admin':
        stations = Setup.objects.all().order_by('date').reverse()
        geojson = JSON.GetGeoJsonStations(stations)
    elif obj.userType == 'is_operator':
        station_access = Access.objects.filter(user_id = obj.id)
        user_access = []
        for station_q in station_access:
            user_access.append(station_q.station_id)
        stations = Setup.objects.filter(id__in = user_access).order_by('date').reverse()
        geojson = JSON.GetGeoJsonStations(stations)
    elif obj.userType == 'is_user':
        station_access = Access.objects.filter(user_id = obj.id)
        user_access = []
        for station_q in station_access:
            user_access.append(station_q.station_id)
        stations = Setup.objects.filter(id__in = user_access).order_by('date').reverse()
        geojson = JSON.GetGeoJsonStations(stations, 'user')

    if stationID != 0:
        station = Setup.objects.get(pk=stationID)
        station_id = station.station_id
        station_city = station.city
        station_status = station.status
        station_table = station.table_name
        if station_status:
            start_time = [station.date.year, station.date.month, station.date.day]
            end_time = "Now"
            end_time_p = datetime.now()
            gps_week, second = cleander_to_gps(end_time_p.year, end_time_p.month, end_time_p.day, 0, 0, 0)
        else:
            start_time = [station.date.year, station.date.month, station.date.day]
            end_time = Deactivate.objects.get(station_id_id = station.pk).date
            gps_week, second = cleander_to_gps(end_time.year, end_time.month, end_time.day, 0, 0, 0)

        d = '''`t, value
                0,0`'''
        hist_data = update_hist(station_table, gps_week, second)
        end_hour = "None"
        for i in range(1, 25):
            if hist_data[-i] > 0:
                end_hour = hist_data[-i]
            break

        if end_hour == "None":
            xPlotData, yPlotData ,zPlotData, tempPlotData = d, d, d, d
        else:
            if end_time == "Now":
                from_time = datetime(end_time_p.year, end_time_p.month, end_time_p.day, end_hour, 0, 0)
                to_time = from_time + timedelta(hours=1)
                from_week, from_second = cleander_to_gps(from_time.year, from_time.month, from_time.day, from_time.hour, 0, 0)
                to_week, to_second = cleander_to_gps(to_time.year, to_time.month, to_time.day, to_time.hour, 0, 0)
            else:
                from_time = datetime(end_time.year, end_time.month, end_time.day, end_hour, 0, 0)
                to_time = from_time + timedelta(hours=1)
                from_week, from_second = cleander_to_gps(from_time.year, from_time.month, from_time.day, from_time.hour, 0, 0)
                to_week, to_second = cleander_to_gps(to_time.year, to_time.month, to_time.day, to_time.hour, 0, 0)
            data = get_data(station_table, from_week, from_second, to_week, to_second)
            xPlotData, yPlotData ,zPlotData, tempPlotData = preparation_plot_data(data)
        if end_time != "Now":
            end_time = str(end_time.year) + ',' + str(end_time.month) + ',' + str(end_time.day)
        return render(request, 'plot.html', dict(geojsonObject=geojson, xPlotData=xPlotData, yPlotData=yPlotData, zPlotData=zPlotData,
                                                 tempPlotData=tempPlotData, StationId=station_id, StationCity=station_city, hist_data = hist_data, start_time=start_time, end_time=end_time))
    else :
        if len(stations) >= 1:
            station = stations[0]
            station_id = station.station_id
            station_city = station.city
            station_status = station.status
            station_table = station.table_name
            if station_status:
                start_time = [station.date.year, station.date.month, station.date.day]
                end_time = "Now"
                end_time_p = datetime.now()
                gps_week, second = cleander_to_gps(end_time_p.year, end_time_p.month, end_time_p.day, 0, 0, 0)
            else:
                start_time = [station.date.year, station.date.month, station.date.day]
                end_time = Deactivate.objects.get(station_id_id = station.pk).date
                gps_week, second = cleander_to_gps(end_time.year, end_time.month, end_time.day, 0, 0, 0)

            d = '''`t, value
                    0,0`'''
            hist_data = update_hist(station_table, gps_week, second)
            end_hour = "None"
            for i in range(1, 25):
                if hist_data[-i] > 0:
                    end_hour = hist_data[-i]
                break

            if end_hour == "None":
                xPlotData, yPlotData ,zPlotData, tempPlotData = d, d, d, d
            else:
                if end_time == "Now":
                    from_time = datetime(end_time_p.year, end_time_p.month, end_time_p.day, end_hour, 0, 0)
                    to_time = from_time + timedelta(hours=1)
                    from_week, from_second = cleander_to_gps(from_time.year, from_time.month, from_time.day, from_time.hour, 0, 0)
                    to_week, to_second = cleander_to_gps(to_time.year, to_time.month, to_time.day, to_time.hour, 0, 0)
                else:
                    from_time = datetime(end_time.year, end_time.month, end_time.day, end_hour, 0, 0)
                    to_time = from_time + timedelta(hours=1)
                    from_week, from_second = cleander_to_gps(from_time.year, from_time.month, from_time.day, from_time.hour, 0, 0)
                    to_week, to_second = cleander_to_gps(to_time.year, to_time.month, to_time.day, to_time.hour, 0, 0)
                data = get_data(station_table, from_week, from_second, to_week, to_second)
                xPlotData, yPlotData ,zPlotData, tempPlotData = preparation_plot_data(data)
            if end_time != "Now":
                end_time = str(end_time.year) + ',' + str(end_time.month) + ',' + str(end_time.day)
            return render(request, 'plot.html', dict(geojsonObject=geojson, xPlotData=xPlotData, yPlotData=yPlotData, zPlotData=zPlotData,
                                                     tempPlotData=tempPlotData, StationId=station_id, StationCity=station_city, hist_data = hist_data, start_time=start_time, end_time=end_time))
        else:
            return render(request, 'no_station_plot.html')

    

@login_required(login_url='signpage')
def map(request):
    obj = request.user
    if obj.userType == 'is_admin':
        stations = Setup.objects.all().order_by('date').reverse()
        geojson = JSON.GetGeoJsonStations(stations)
    elif obj.userType == 'is_operator':
        station_access = Access.objects.filter(user_id = obj.id)
        user_access = []
        for station_q in station_access:
            user_access.append(station_q.station_id)
        stations = Setup.objects.filter(id__in = user_access).order_by('date').reverse()
        geojson = JSON.GetGeoJsonStations(stations)
    elif obj.userType == 'is_user':
        station_access = Access.objects.filter(user_id = obj.id)
        user_access = []
        for station_q in station_access:
            user_access.append(station_q.station_id)
        stations = Setup.objects.filter(id__in = user_access).order_by('date').reverse()
        geojson = JSON.GetGeoJsonStations(stations, 'user')

    if len(stations) >= 1:       
        return render(request, 'map.html', dict(geojsonObject=geojson))
    else:
        return render(request, 'no_station_map.html')

    
# def my_handler404(request, exception):
#     return render(request, '404.html', status=404)
