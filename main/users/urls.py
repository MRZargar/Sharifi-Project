from django.urls import path
from .views import SignUpView, sucess_signup




urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/sucess',sucess_signup ,name='sucess'),
]
