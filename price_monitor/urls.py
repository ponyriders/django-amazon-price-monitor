from django.conf.urls import patterns, url, include

from price_monitor.views import AngularIndexView, ProductListAndCreateView

urlpatterns = patterns(
    'price_monitor.views',
    url(r'^page/(?P<page>\d+)/$', ProductListAndCreateView.as_view(), name='monitor_view'),
    url(r'^$', ProductListAndCreateView.as_view(), name='monitor_view'),
    url(r'^subscription/delete/(?P<public_id>[a-z0-9\-]{36})/$', 'delete_subscription_view', name='delete_subscription_view'),
    url(r'^api/', include('price_monitor.api.urls')),
    url(r'^angular/$', AngularIndexView.as_view(), name='angular_view'),
)
