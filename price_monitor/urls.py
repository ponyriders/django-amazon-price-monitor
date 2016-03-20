from django.conf.urls import include, url

from price_monitor.views import AngularIndexView

urlpatterns = [
    url(r'^$', AngularIndexView.as_view(), name='angular_view'),
    url(r'^api/', include('price_monitor.api.urls')),
]
