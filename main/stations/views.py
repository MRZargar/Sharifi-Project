from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import StationSetup, StationDeactivate
from .models import Setup, Image, Deactivate
from django.http import JsonResponse


def station_setup(request):
	if  request.method == 'POST':
		form = StationSetup(request.POST, request.FILES)
		files = request.FILES.getlist('images')
		if form.is_valid():
			station_name = form.cleaned_data['station_name']
			address = form.cleaned_data['address']
			description = form.cleaned_data['description']
			operator_name = request.user.username
			station_obj = Setup.objects.create(station_name=station_name,
						 address=address,
						 description=description,
						 operator_name=operator_name,
						 status=True)
			for f in files:
				Image.objects.create(setup=station_obj, images=f)
			return redirect('success')
	else:
		form = StationSetup()
	return render(request, 'setupStation.html', {'form':form})



def success(request):
	return HttpResponse('success')



def station_list(request):
	if request.method == "GET":
		station_list = Setup.objects.all()
		return render(request, 'station_list.html', {'station_list':station_list})


def station_detail(request, pk):
	if request.method == "GET":
		global station
		station = Setup.objects.get(pk = pk)
		images = Image.objects.filter(setup_id = pk)
		return render(request, 'station_detail.html', {'station': station,
													   'images': images})
	if request.method == "POST":
		form = StationDeactivate(request.POST)
		if form.is_valid():
			operator_name = request.user.username
			station_name = Setup.objects.get(station_name = station.station_name)
			description = form.cleaned_data['description']

			this_station = Setup.objects.get(id = station.id)
			this_station.status = False
			this_station.save()
			Deactivate.objects.create(operator_name=operator_name, 
					                  station_name=station_name,
					                   description=description)
			return redirect('success')
		else:
			form = StationDeactivate()
		return render(request, 'station_detail.html', {'form': form})


