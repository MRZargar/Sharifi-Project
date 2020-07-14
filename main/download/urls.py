from django.urls import path
from .views import download	



urlpatterns = [

	path("file/link/<int:pk>", download, name="downloads_files"),
	
]