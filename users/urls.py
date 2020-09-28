from django.urls import path
from .views import (
    SignUpView,
    success_signup,
    SignUpView2,
    AuthorUpdate,
    success_edit,
    account_activation_sent,
    activate,
    profile_view,
    active_user_page,
    access_station,
    user_delete
) 
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('signup/<int:pk>', SignUpView, name='signup'),
    path('active/users/<int:pk>', active_user_page, name="active_user_page"),
    path('active/users/access/<int:pk>', access_station, name="access_station"),
    path('active/users/delete/user/<int:pk>', user_delete, name="user_delete"),
    path('signup/sucess',success_signup ,name='success'),
    path('signup/user/', SignUpView2, name='signup2'),
    path('edit/<int:pk>', login_required(AuthorUpdate.as_view()), name="EditUserName"),
    path('changed', success_edit, name="success_edit"),
    path('account/activation/sent/', account_activation_sent, name='account_activation_sent'),
    path('activate/?P<uidb64>[0-9A-Za-z_\-]+/?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}/', activate, name='activate'),
    path('profile/<int:pk>', profile_view, name='profile')

]



