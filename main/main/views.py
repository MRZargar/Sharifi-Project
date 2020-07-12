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

User = get_user_model()



# Convet time to gps week and seconds
def cleander_to_gps(year, month, day, hour, minute, second):
    time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    all_seconds = to_gps(time) - 18
    week = int(all_seconds/604800)
    second = all_seconds % 604800 
    return (week, second)


def home_page(request):
    return render(request, "Signin.html")

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
                return redirect("UserProfile", pk=pk)
            elif user.userType == 'is_operator':
                    auth.login(request, user)
                    return redirect("OperatorProfile", pk=pk)
            elif user.userType == 'is_admin':
                    auth.login(request, user)
                    return redirect("AdminProfile", pk=pk)
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
        station_name = request.GET['StationName']
        station = Setup.objects.get(station_name=station_name)
        date = request.GET['Date']
        to_date = int(request.GET['Hour'])
        from_date = to_date - 1
        date = date.split("/")
        from_week, from_second = cleander_to_gps(date[0], date[1], date[2], from_date, 0, 0)
        to_week, to_second = from_week ,from_second + 3600
        station_id = station.pk
        x, y ,z, temp = 0, 0, 0, 0
        return JsonResponse({'xPlotData':x, 'yPlotData':y, 'zPlotData':z, 'tempPlotData':temp}, status=200)

@login_required(login_url='signpage')
def histogram_update(request):
    if request.method == "GET":
        station_name = request.GET['StationName']
        from_date = request.GET['Date']
        station = Setup.objects.get(station_name=station_name)
        from_date = from_date.split("/")
        from_time = (datetime(int(from_date[0]), int(from_date[1]), int(from_date[2]))) 
        to_time = from_time + timedelta(days=1)
        from_week, from_second = cleander_to_gps(from_time.year, from_time.month, from_time.day, 0, 0, 0)
        to_week, to_second = cleander_to_gps(to_time.year, to_time.month, to_time.day, 0, 0, 0)
        hist_data = [100, 100, 100, 70, 50, 100, 100, 0, 20, 100, 40, 10, 100, 100, 100, 0, 30, 40, 50, 60, 70, 80, 90, 100]
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

    if stationID != 12345698722222222222254654879874102587932:
        station = Setup.objects.get(pk=stationID)
        station_name = station.station_name
        station_status = station.status
        if station_status:
            start_time = [station.date.year, station.date.month, station.date.day]
            end_time = "Now"
        else:
            start_time = [station.date.year, station.date.month, station.date.day]
            end_time = Deactivate.objects.get(station_name_id = station.pk).date
            end_time = [end_time.year, end_time.month, end_time.day]

        d = '''`t, value
                0,0`'''
        hist_data = [100, 100, 100, 70, 50, 100, 100, 100, 20, 100, 40, 10, 100, 100, 100, 0, 50, 100, 100, 100, 20, 100, 40, 10]
        xPlotData, yPlotData ,zPlotData, tempPlotData = d, d, d, d

        return render(request, 'plot.html', dict(geojsonObject=geojson, xPlotData=xPlotData, yPlotData=yPlotData, zPlotData=zPlotData,
                                                 tempPlotData=tempPlotData, StationName=station_name, hist_data = hist_data, start_time=start_time, end_time=end_time))
    else :
        if len(stations) >= 1:
            station = stations[0]
            station_name = station.station_name
            station_status = station.status
            if station_status:
                start_time = [station.date.year, station.date.month, station.date.day]
                end_time = "Now"
            else:
                start_time = [station.date.year, station.date.month, station.date.day]
                end_time = Deactivate.objects.get(station_name_id = station.pk).date
                end_time = [end_time.year, end_time.month, end_time.day]

            # ax, ay, az = JSON.GetPoltData(get from api)
            # hist = JSON.GetHistData(get from api)
            d = '''`t, value
                    0,0`'''
            hist_data = [100, 100, 100, 70, 50, 100, 100, 100, 20, 100, 40, 10, 100, 100, 100, 0, 50, 100, 100, 100, 20, 100, 40, 10]
            xPlotData, yPlotData ,zPlotData, tempPlotData = d, d, d, d
            return render(request, 'plot.html', dict(geojsonObject=geojson, xPlotData=xPlotData, yPlotData=yPlotData, zPlotData=zPlotData,
                                                     tempPlotData=tempPlotData, StationName=station_name, hist_data = hist_data, start_time=start_time, end_time=end_time))
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
            station_list.append(station.station_name)
        return JsonResponse({'stations_list': station_list}, status=200)

    elif request.method == "GET" and request.GET['method'] == "download":
        stations_name = request.GET.getlist('StaionsName[]')
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
            for station in stations_name:
                stations.append(Setup.objects.get(station_name=station))
            for d_station in stations:
                station_id = d_station.pk
                for i in range(delta.days + 1):
                    date = from_time + timedelta(days=i)
                    for j in hours:
                        from_week, from_second = cleander_to_gps(date.strftime("%Y"), date.strftime("%m"), date.strftime("%d"), (int(j)-1), 0, 0)
                        to_week, to_second = from_week, from_second + 3600
                        print("station_id : ", station_id)
                        print("from_week : ", from_week)
                        print("from_second : ", from_second)
                        print("to_week : ", to_week)
                        print("to_second : ", to_second)
            return JsonResponse({}, status=200)
