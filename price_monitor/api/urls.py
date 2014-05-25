from django.conf.urls import patterns, url

from price_monitor.api.views.ProductListView import ProductListView


urlpatterns = patterns(
    '',
    url(r'^products/$', ProductListView.as_view(), name='userpost-list'),
)
