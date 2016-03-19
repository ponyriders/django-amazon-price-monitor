from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'glue_auth/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
)
