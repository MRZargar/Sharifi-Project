from django.urls import path
from .views import(station_setup, 
				   station_list,
				   station_detail,
				   delete_station,
				   station_deactive
)	

urlpatterns = [
	path('setup', station_setup, name="station_setup"),
	path('', station_list, name="station_list"),
	path('<int:pk>', station_detail, name="station_detail"),
	path('station/delete/<int:pk>', delete_station, name='station_delete'),
	path('station/deactive/<int:pk>', station_deactive, name="deactive_station")
]