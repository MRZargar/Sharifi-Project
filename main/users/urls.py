from django.urls import path
from .views import (
    SignUpView,
    success_signup,
    SignUpView2,
    AuthorUpdate,
    success_edit
) 
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('signup/<int:pk>', login_required(SignUpView.as_view()), name='signup'),
    path('signup/sucess',login_required(success_signup) ,name='success'),
    path('signup2/', SignUpView2.as_view(), name='signup2'),
    path('edit/<int:pk>', login_required(AuthorUpdate.as_view()), name="EditUserName"),
    path('changed', success_edit, name="success_edit"),
]