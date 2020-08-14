
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
    inbox_message_view,
    plot_update,
    histogram_update
)
urlpatterns = [
    path('', home_page, name='homePage'),
    path('users/signin/', signpage, name='signpage'),
    path('admin/', admin.site.urls),
    path('users/1/<int:pk>', UserProfile, name='UserProfile'),
    path('users/2/<int:pk>', OperatorProfile, name='OperatorProfile'),
    path('users/3/<int:pk>', AdminProfile, name='AdminProfile'),
    path('signout', signout, name='signout'),
    path("plot/<int:stationID>", plot, name='plot'),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('map/', map, name='map'),
    path('stations/', include('stations.urls')),
    path('message', include('message.urls')),
    path('inbox/message/<int:pk>', inbox_message_view, name='inbox_message_count'),
    path("plot/update/", plot_update, name="update_plot"),
    path("histogram/update/", histogram_update, name="update_histogram"),
    path('download/', include('download.urls')),

]



if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)