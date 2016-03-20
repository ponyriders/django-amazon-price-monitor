"""URL definitions for the glue project."""
from django.conf.urls import include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('glue_auth.urls')),
    url(r'^', include('price_monitor.urls')),
]
