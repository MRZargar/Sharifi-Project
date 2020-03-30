
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
    plot_page,
    plots_map_page,
    map,
    ttest
)
urlpatterns = [
    path('', signpage, name='signpage'),
    path('admin/', admin.site.urls),
    path('users/1', login_required(UserProfile), name='UserProfile'),
    path('users/2', login_required(OperatorProfile), name='OperatorProfile'),
    path('users/3', login_required(AdminProfile), name='AdminProfile'),
    path('signout/', signout, name='signout'),
    path('plot/', plot_page, name='plot'),
    path('plots_map/', plots_map_page, name='plots'),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('map/', map, name='map'),
    path('test/', ttest, name='test')
]