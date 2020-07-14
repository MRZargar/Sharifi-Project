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
				station_name = form.cleaned_data['station_name']
				for_character_id = form.cleaned_data['for_character_id']
				address = form.cleaned_data['address']
				latitude = form.cleaned_data['latitude']
				longitude = form.cleaned_data['longitude']
				description = form.cleaned_data['description']
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
				station_obj = Setup.objects.create(station_name=station_name,
							for_character_id=for_character_id,
							 address=address,
							 description=description,
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
	form = StationDeactivate()
	return render(request, 'station_list.html', {'station_list':station_list, 'form':form})


@login_required(login_url='signpage')
def station_deactive(request, pk):
	obj = request.user
	if obj.userType == 'is_user':
		raise PermissionDenied
	if request.method == "POST":
		form = StationDeactivate(request.POST)
		station_name = request.POST['StationName']
		operator = request.user
		description = request.POST['Discribtion']
		if len(description) == 0 and obj.userType =='is_operator':
			return JsonResponse({}, status=400)
		else:
			this_station = Setup.objects.get(station_name=station_name)
			Deactivate.objects.create(operator=operator, 
					                  station_name=this_station,
					                   description=description)
			this_station.status = False
			Raspberry.objects.get(raspberryID=this_station.raspberryID).delete()
			this_station.save()
			MyUserType = obj.userType
			return JsonResponse({"user_type": MyUserType}, status=200)


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
		station_name = request.POST["StationName"]
		Setup.objects.get(station_name=station_name).delete()
		return JsonResponse({}, status=200)



