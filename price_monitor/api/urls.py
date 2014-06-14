from django.conf.urls import patterns, url

from price_monitor.api.views.ProductListView import ProductListView
from price_monitor.api.views.ProductCRUDView import ProductCRUDView
from price_monitor.api.views.SubscriptCRUDView import SubscriptionCRUDView
from price_monitor.api.views.SubscriptionListView import SubscriptionListView


urlpatterns = patterns(
    '',
    url(r'^products/$', ProductListView.as_view(), name='product-list'),
    url(r'^subscriptions/$', SubscriptionListView.as_view(), name='subscription-list'),
    url(r'^product-crud/?$', ProductCRUDView.as_view(), name='api_product_crud'),
    url(r'^subscription-crud/?$', SubscriptionCRUDView.as_view(), name='api_subscription_crud'),
)
