from django.urls import path
from .views import (send_message,
					inbox,
					send,
					send_detail,
					inbox_detail
)

urlpatterns = [
	path("<int:pk>/", send_message, name="messages"),
	path("<int:pk>/inbox", inbox, name="inbox"),
	path("<int:pk>/send", send, name="send"),
	path("<slug:slug>/send/detail", send_detail, name="send_detail"),
	path("<slug:slug>/inbox/detail", inbox_detail, name="inbox_detail")
]
