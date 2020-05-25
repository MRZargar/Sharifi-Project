
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf.urls import handler403, handler404
from django.conf import settings
from django.conf.urls.static import static



from .views import(
    home_page,
    signpage,
    signout,
    UserProfile,
    OperatorProfile,
    AdminProfile,
    plot,
    map,
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
    path('stations/', include('stations.urls')),
    path('message', include('message.urls'))

]



if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)