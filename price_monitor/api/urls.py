from django.conf.urls import patterns, url, include

from price_monitor.api.views.ProductListView import ProductListView


urlpatterns = patterns('',
    url(r'^products/$', ProductListView.as_view(), name='userpost-list'),
)
