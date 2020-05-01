from django.urls import path
from .views import(station_setup,
				   success, 
				   station_list,
				   station_detail
)	

urlpatterns = [
	path('setup', station_setup, name="station_setup"),
	path('success', success, name="success"),
	path('', station_list, name="station_list"),
	path('<int:pk>', station_detail, name="station_detail"),
]