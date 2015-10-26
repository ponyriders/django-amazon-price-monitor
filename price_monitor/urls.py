from django.conf.urls import patterns, url, include

from price_monitor.views import AngularIndexView

urlpatterns = patterns(
    'price_monitor.views',
    url(r'^$', AngularIndexView.as_view(), name='angular_view'),
    url(r'^api/', include('price_monitor.api.urls')),
)
