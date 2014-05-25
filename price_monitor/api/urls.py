from django.conf.urls import patterns, url

from price_monitor.api.views.ProductCRUDView import ProductCRUDView
from price_monitor.api.views.SubscriptCRUDView import SubscriptionCRUDView


urlpatterns = patterns(
    '',
    # url(r'^products/$', ProductListView.as_view(), name='userpost-list'),
    url(r'^product-crud/$', ProductCRUDView.as_view(), name='api_product_crud'),
    url(r'^subscription-crud/$', SubscriptionCRUDView.as_view(), name='api_subscription_crud'),
)
