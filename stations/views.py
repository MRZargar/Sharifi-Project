from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import StationSetup2, StationDeactivate
from .models import Setup, Image, Deactivate, Raspberry, Access
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from users.models import CustomUser
from decimal import Decimal
import datetime
from json import dumps

### Setup station view ###
@login_required(login_url='signpage')
def station_setup(request):
	obj = request.user
	if obj.userType == 'is_user':
		raise PermissionDenied
	elif  request.method == 'POST':
		Raspberry_Id = Raspberry.objects.all()
		stations_all = Setup.objects.all()
		st_count = stations_all.count()
		id_list = []
		if st_count == 0:
			for Id in Raspberry_Id:
				id_list.append((Id.raspberryID, Id.raspberryID))
		else:
			for Id in Raspberry_Id:
				temp = True
				for st in stations_all:
					if Id.raspberryID == st.raspberryID and st.status == True:
						temp = False
						continue
				if temp:
					id_list.append((Id.raspberryID, Id.raspberryID))
		new_choices = tuple(id_list)
		form = StationSetup2(request.POST, request.FILES , new_choices=new_choices)
		files = request.FILES.getlist('images')
		if len(files) == 0:
			messages.error(request, "Please upload image or images", extra_tags='image')
			return render(request, 'setupStation.html', {'form':form})
		else:
			if form.is_valid():
				city = form.cleaned_data['city']
				station_id = form.cleaned_data['station_id']
				station_id = station_id.lower()
				split_first_station_id = station_id[0:4]
				split_second_station_id = station_id[4:8]
				if not station_id.isascii():
					messages.error(request, "Please use English letters", extra_tags='station_id_error')
					return render(request, 'setupStation.html', {'form':form})
				elif not split_first_station_id.isalpha():
					messages.error(request, "The first four words must be alphanumeric characters", extra_tags='station_id_error')
					return render(request, 'setupStation.html', {'form':form})
				elif not split_second_station_id.isdigit():
					messages.error(request, "The second four words must be numbers", extra_tags='station_id_error')
					return render(request, 'setupStation.html', {'form':form})
				address = form.cleaned_data['address']
				sensor_type = form.cleaned_data['sensor_type']
				latitude = form.cleaned_data['latitude']
				longitude = form.cleaned_data['longitude']
				owner = form.cleaned_data['owner']
				raspberryID = form.cleaned_data['raspberryID']
				operator = request.user
				lat = Decimal(str(latitude))
				lon = Decimal(str(longitude))
				if abs(lat.as_tuple().exponent) < 6 and abs(lon.as_tuple().exponent) < 6:
					messages.error(request, "Your number must be six decimal places", extra_tags='lat')
					messages.error(request, "Your number must be six decimal places", extra_tags='lon')
					return render(request, 'setupStation.html', {'form':form})
				elif abs(lat.as_tuple().exponent) < 6:
					messages.error(request, "Your number must be six decimal places", extra_tags='lat')
					return render(request, 'setupStation.html', {'form':form})
				elif abs(lon.as_tuple().exponent) < 6:
					messages.error(request, "Your number must be six decimal places", extra_tags='lon')
					return render(request, 'setupStation.html', {'form':form})
				station_obj = Setup.objects.create(city=city,
							 station_id=station_id,
							 address=address,
							 sensor_type=sensor_type,
							 owner=owner,
							 operator=operator,
							 latitude = latitude,
							 longitude = longitude,
							 raspberryID = raspberryID,
							 status=True)
				if obj.userType == 'is_operator':
					Access.objects.create(user=obj, station=station_obj)
				for f in files:
					Image.objects.create(setup=station_obj, images=f)
				return redirect('station_list')
	else:
		Raspberry_Id = Raspberry.objects.all()
		stations_all = Setup.objects.all()
		st_count = stations_all.count()
		id_list = []
		if st_count == 0:
			for Id in Raspberry_Id:
				id_list.append((Id.raspberryID, Id.raspberryID))
		else:
			for Id in Raspberry_Id:
				temp = True
				for st in stations_all:
					if Id.raspberryID == st.raspberryID and st.status == True:
						temp = False
				if temp:
					id_list.append((Id.raspberryID, Id.raspberryID))
		new_choices = tuple(id_list)
		form = StationSetup2(new_choices=new_choices)
	return render(request, "setupStation.html", {'form':form})


new_choices=(('is_user', 'user'),('is_operator', 'operator'),)

### station list view ###
@login_required(login_url='signpage')
def station_list(request):
	UTC_time = datetime.timedelta(hours=4, minutes=30, seconds=0)
	obj = request.user
	if obj.userType == 'is_user':
		raise PermissionDenied
	if obj.userType == 'is_operator':
		station_access = Access.objects.filter(user_id = obj.id)
		user_access = []
		for station_q in station_access:
			user_access.append(station_q.station_id)
		station_list = Setup.objects.filter(id__in = user_access).order_by('date').reverse()
	elif obj.userType == 'is_admin':
		station_list = Setup.objects.all().order_by('date').reverse()
	healths = []
	for station in station_list:
		if station.status == True:
		    db_time = datetime.datetime(station.health_time.year, station.health_time.month, station.health_time.day, station.health_time.hour, station.health_time.minute, station.health_time.second)
		    db_time += UTC_time
		    time = datetime.datetime.now() - db_time
		    if time.total_seconds() > 15:
		        health = 2
		    else:
		        health = station.health
		    healths.append([station.station_id, health])
	healths = dumps(healths)
	form = StationDeactivate()
	return render(request, 'station_list.html', {'station_list':station_list, 'form':form, 'health':healths})


@login_required(login_url='signpage')
def station_deactive(request, pk):
	obj = request.user
	if obj.userType == 'is_user':
		raise PermissionDenied
	if request.method == "POST":
		form = StationDeactivate(request.POST)
		stations_id = request.POST.getlist('StationIds[]')
		print(stations_id)
		operator = request.user
		description = request.POST['Discribtion']
		if len(description) == 0 and obj.userType =='is_operator':
			return JsonResponse({}, status=400)
		else:
			for station_id in stations_id:
				this_station = Setup.objects.get(station_id=station_id)
				Deactivate.objects.create(operator=operator, 
						                  station_id=this_station,
						                   description=description)
				this_station.status = False
				Raspberry.objects.get(raspberryID=this_station.raspberryID).delete()
				this_station.save()
			return JsonResponse({}, status=200)


### station detail view ###
@login_required(login_url='signpage')
def station_detail(request, pk):
	obj = request.user
	if obj.userType == 'is_user':
		raise PermissionDenied
	station = Setup.objects.get(pk = pk)
	images = Image.objects.filter(setup_id = pk)
	if station.status == False:
		deactive = Deactivate.objects.get(station_name_id = pk)
		return render(request, 'station_detail.html', {'station': station,
												   'images': images, 'deactive':deactive})
	else:
		return render(request, 'station_detail.html', {'station': station,
												   'images': images})


@login_required(login_url='signpage')
def delete_station(request, pk):
	obj = request.user
	if obj.userType != 'is_admin':
		raise PermissionDenied
	if request.method == "POST":
		station_ids= request.POST.getlist("StationIds[]")
		for station_id in station_ids:
			Setup.objects.get(station_id=station_id).delete()
		return JsonResponse({}, status=200)



