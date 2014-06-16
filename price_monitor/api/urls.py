from django.conf.urls import patterns, url

from price_monitor.api.views.EmailNotificationListView import EmailNotificationListView
from price_monitor.api.views.PriceListView import PriceListView
from price_monitor.api.views.ProductListView import ProductListView
from price_monitor.api.views.ProductCRUDView import ProductCRUDView
from price_monitor.api.views.SubscriptCRUDView import SubscriptionCRUDView
from price_monitor.api.views.SubscriptionListView import SubscriptionListView


urlpatterns = patterns(
    '',
    url(r'^email-notifications/$', EmailNotificationListView.as_view(), name='email_notification_list'),
    url(r'^products/(?P<asin>[0-9a-zA-Z_-]+)/prices/$', PriceListView.as_view(), name='userpost-list'),
    url(r'^products/$', ProductListView.as_view(), name='product_list'),
    url(r'^subscriptions/$', SubscriptionListView.as_view(), name='subscription_list'),
    url(r'^product-crud/?$', ProductCRUDView.as_view(), name='api_product_crud'),
    url(r'^subscription-crud/?$', SubscriptionCRUDView.as_view(), name='api_subscription_crud'),
)
