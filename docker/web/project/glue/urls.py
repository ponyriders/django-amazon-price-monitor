from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^void/', include(admin.site.urls)),
    url(r'^', include('glue_auth.urls', namespace='glue_auth')),
    url(r'^', include('price_monitor.urls')),
)
