from django.conf.urls import patterns, url

from price_monitor.api.views.EmailNotificationListView import EmailNotificationListView
from price_monitor.api.views.PriceListView import PriceListView
from price_monitor.api.views.ProductListView import ProductListView
from price_monitor.api.views.ProductRetrieveView import ProductRetrieveView
from price_monitor.api.views.SubscriptionRetrieveView import SubscriptionRetrieveView
from price_monitor.api.views.SubscriptionListView import SubscriptionListView


urlpatterns = patterns(
    '',
    url(r'^email-notifications/$', EmailNotificationListView.as_view(), name='api_email_notification_list'),
    url(r'^products/(?P<asin>[0-9a-zA-Z_-]+)/prices/$', PriceListView.as_view(), name='api_product_price_list'),
    url(r'^products/(?P<asin>[0-9a-zA-Z_-]+)/$', ProductRetrieveView.as_view(), name='api_product_list'),
    url(r'^products/$', ProductListView.as_view(), name='api_product_list'),
    url(r'^subscriptions/(?P<public_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', SubscriptionRetrieveView.as_view(), name='api_subscription_retrieve'),
    url(r'^subscriptions/$', SubscriptionListView.as_view(), name='api_subscription_list'),
)
