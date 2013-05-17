from django.conf.urls import patterns, url

from price_monitor.views import ProductCreateView

urlpatterns = patterns('',
    url(r'^create/$', ProductCreateView.as_view()),
)
