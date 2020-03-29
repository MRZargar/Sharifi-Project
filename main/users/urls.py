from django.urls import path
from .views import SignUpView, sucess_signup, SignUpView2
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('signup/', login_required(SignUpView.as_view()), name='signup'),
    path('signup/sucess',login_required(sucess_signup) ,name='success'),
    path('signup2/', login_required(SignUpView2.as_view()), name='signup2'),
]
