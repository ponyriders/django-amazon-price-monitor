"""URL definitions for the glue_auth module."""
from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login


app_name = 'glue_auth'
urlpatterns = [
    url(r'^login/$', login, {'template_name': 'glue_auth/login.html'}, name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),
]
