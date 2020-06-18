from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import StationSetup2, StationDeactivate
from .models import Setup, Image, Deactivate, Raspberry
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from users.models import CustomUser


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
		print(new_choices)
		form = StationSetup2(request.POST, request.FILES , new_choices=new_choices)
		files = request.FILES.getlist('images')
		if len(files) == 0:
			messages.error(request, "Please upload image or images")
			return render(request, 'setupStation.html', {'form':form})
		else:
			if form.is_valid():
				station_name = form.cleaned_data['station_name']
				address = form.cleaned_data['address']
				latitude = form.cleaned_data['latitude']
				longitude = form.cleaned_data['longitude']
				description = form.cleaned_data['description']
				raspberryID = form.cleaned_data['raspberryID']
				operator_id = request.user
				station_obj = Setup.objects.create(station_name=station_name,
							 address=address,
							 description=description,
							 operator_id=operator_id,
							 latitude = latitude,
							 longitude = longitude,
							 raspberryID = raspberryID,
							 status=True)
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
		print(new_choices)
		form = StationSetup2(new_choices=new_choices)
	return render(request, 'setupStation.html', {'form':form})

new_choices=(('is_user', 'user'),('is_operator', 'operator'),)
### station list view ###
@login_required(login_url='signpage')
def station_list(request):
	obj = request.user
	if obj.userType == 'is_user':
		raise PermissionDenied
	elif request.method == "GET":
		if obj.userType == 'is_operator':
			station_list = Setup.objects.filter(operator_id = obj.id).order_by('date').reverse()
		elif obj.userType == 'is_admin':
			station_list = Setup.objects.all().order_by('date').reverse()
		return render(request, 'station_list.html', {'station_list':station_list})



### station detail view ###
@login_required(login_url='signpage')
def station_detail(request, pk):
	obj = request.user
	if obj.userType == 'is_user':
		raise PermissionDenied

	if request.method == "GET":
		global station
		station = Setup.objects.get(pk = pk)
		images = Image.objects.filter(setup_id = pk)
		if station.status == False:
			deactive = Deactivate.objects.get(station_name_id = pk)
			return render(request, 'station_detail.html', {'station': station,
													   'images': images, 'deactive':deactive})
		else:
			return render(request, 'station_detail.html', {'station': station,
													   'images': images})
	if request.method == "POST":
		form = StationDeactivate(request.POST)
		if form.is_valid():
			operator_id = request.user
			station_name = Setup.objects.get(station_name = station.station_name)
			description = form.cleaned_data['description']

			this_station = Setup.objects.get(id = station.id)
			Deactivate.objects.create(operator_id=operator_id, 
					                  station_name=station_name,
					                   description=description)
			this_station.status = False
			this_station.save()
			return redirect('station_list')
		else:
			form = StationDeactivate()
		return render(request, 'station_detail.html', {'form': form})


