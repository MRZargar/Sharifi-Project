from django.urls import path
from .views import download, requests_list



urlpatterns = [
	path("file/link/<int:pk>", download, name="downloads_files"),
	path("requests/link/<int:pk>", requests_list, name="request_list")
	
]