
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf.urls import handler403, handler404

from .views import(
    home_page,
    signpage,
    signout,
    UserProfile,
    OperatorProfile,
    AdminProfile,
    plot,
    map,
    ttest,
)
urlpatterns = [
    path('', signpage, name='signpage'),
    path('admin/', admin.site.urls),
    path('users/1/<int:pk>', UserProfile, name='UserProfile'),
    path('users/2/<int:pk>', OperatorProfile, name='OperatorProfile'),
    path('users/3/<int:pk>', AdminProfile, name='AdminProfile'),
    path('signout', signout, name='signout'),
    path('plot/', plot, name='plot'),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('map/', map, name='map'),
    path('test/', ttest, name='test')
]