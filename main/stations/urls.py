from django.urls import path
from .views import(station_setup, 
				   station_list,
				   station_detail,
				   delete_station
)	

urlpatterns = [
	path('setup', station_setup, name="station_setup"),
	path('', station_list, name="station_list"),
	path('<int:pk>', station_detail, name="station_detail"),
	path('statton/delete/<int:pk>', delete_station, name='station_delete')
]