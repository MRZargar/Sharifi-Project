
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


from .views import(
    home_page,
    signpage,
    signout,
    UserProfile,
    OperatorProfile,
    AdminProfile,
    plot_page,
    plots_map_page,
)
urlpatterns = [
    path('', home_page, name='home_page'),
    path('admin/', admin.site.urls),
    path('signin', signpage, name='signpage'),
    path('users/1', login_required(UserProfile), name='UserProfile'),
    path('users/2', login_required(OperatorProfile), name='OperatorProfile'),
    path('users/3', login_required(AdminProfile), name='AdminProfile'),
    path('signout/', signout, name='signout'),
    path('plot/', plot_page, name='plot'),
    path('plots/', plots_map_page, name='plots'),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
]
