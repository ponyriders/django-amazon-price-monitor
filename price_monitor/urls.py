from django.conf.urls import patterns, url

from price_monitor.views import ProductListAndCreateView

urlpatterns = patterns('',
    url(r'^page/(?P<page>\d+)/$', ProductListAndCreateView.as_view(), name='monitor_view'),
    url(r'^$', ProductListAndCreateView.as_view(), name='monitor_view'),
    url(r'^charts-demo/$', 'price_monitor.views.charts_demo_view', name='charts_demo_view'),
)
