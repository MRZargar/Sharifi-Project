from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import StationSetup, StationDeactivate
from .models import Setup, Image, Deactivate
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages


### Setup station view ###
@login_required(login_url='signpage')
def station_setup(request):
	obj = request.user
	if obj.userType == 'is_user':
		raise PermissionDenied
	elif  request.method == 'POST':
		form = StationSetup(request.POST, request.FILES)
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
				operator_id = request.user.id
				operator_name = request.user.username
				station_obj = Setup.objects.create(station_name=station_name,
							 address=address,
							 description=description,
							 operator_id=operator_id,
							 operator_name=operator_name,
							 latitude = latitude,
							 longitude = longitude,
							 status=True)
				for f in files:
					Image.objects.create(setup=station_obj, images=f)
				return redirect('station_list')
	else:
		form = StationSetup()
	return render(request, 'setupStation.html', {'form':form})


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
			operator_name = request.user.username
			station_name = Setup.objects.get(station_name = station.station_name)
			description = form.cleaned_data['description']

			this_station = Setup.objects.get(id = station.id)
			Deactivate.objects.create(operator_name=operator_name, 
					                  station_name=station_name,
					                   description=description)
			this_station.status = False
			this_station.save()
			return redirect('station_list')
		else:
			form = StationDeactivate()
		return render(request, 'station_detail.html', {'form': form})


