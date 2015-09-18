from django.conf.urls import patterns, url

from .views.EmailNotificationListView import EmailNotificationListView
from .views.PriceListView import PriceListView
from .views.ProductListView import ProductListView
from .views.ProductCreateRetrieveUpdateDestroyAPIView import ProductCreateRetrieveUpdateDestroyAPIView
from .views.SubscriptionRetrieveView import SubscriptionRetrieveView
from .views.SubscriptionListView import SubscriptionListView


urlpatterns = patterns(
    '',
    url(r'^email-notifications/$', EmailNotificationListView.as_view(), name='api_email_notification_list'),
    url(r'^products/(?P<asin>[0-9a-zA-Z_-]+)/prices/$', PriceListView.as_view(), name='api_product_price_list'),
    url(r'^products/(?P<asin>[0-9a-zA-Z_-]+)/$', ProductCreateRetrieveUpdateDestroyAPIView.as_view(), name='api_product_retrieve'),
    url(r'^products/$', ProductListView.as_view(), name='api_product_list'),
    url(
        r'^subscriptions/(?P<public_id>(:public_id|[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}))/$',
        SubscriptionRetrieveView.as_view(),
        name='api_subscription_retrieve'
    ),
    url(r'^subscriptions/$', SubscriptionListView.as_view(), name='api_subscription_list'),
)
