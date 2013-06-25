from django.conf.urls import patterns, url

from price_monitor.views import ProductListAndCreateView

urlpatterns = patterns('',
    url(r'^$', ProductListAndCreateView.as_view(), name='monitor_view'),
)
