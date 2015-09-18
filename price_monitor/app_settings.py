from django.conf import settings
from django.utils.translation import ugettext_lazy


# global AWS access settings
PRICE_MONITOR_AWS_ACCESS_KEY_ID = getattr(settings, 'PRICE_MONITOR_AWS_ACCESS_KEY_ID', '')
PRICE_MONITOR_AWS_SECRET_ACCESS_KEY = getattr(settings, 'PRICE_MONITOR_AWS_SECRET_ACCESS_KEY', '')
PRICE_MONITOR_AMAZON_PRODUCT_API_REGION = getattr(settings, 'PRICE_MONITOR_AMAZON_PRODUCT_API_REGION', '')
PRICE_MONITOR_AMAZON_PRODUCT_API_ASSOC_TAG = getattr(settings, 'PRICE_MONITOR_AMAZON_PRODUCT_API_ASSOC_TAG', '')

# server infrastructural settings
# serve the product images via HTTPS
PRICE_MONITOR_IMAGES_USE_SSL = getattr(settings, 'PRICE_MONITOR_IMAGES_USE_SSL', True)
# HTTPS host to use for getting the images. Seems to be https://images-<REGION>.ssl-images-amazon.com.
PRICE_MONITOR_AMAZON_SSL_IMAGE_DOMAIN = getattr(settings, 'PRICE_MONITOR_AMAZON_SSL_IMAGE_DOMAIN', 'https://images-eu.ssl-images-amazon.com')

# synchronization settings
# refresh product after 12 hours
PRICE_MONITOR_AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES = getattr(settings, 'PRICE_MONITOR_AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES', 12 * 60)

# notification settings
# time after when to notify about a subscription again
PRICE_MONITOR_SUBSCRIPTION_RENOTIFICATION_MINUTES = getattr(settings, 'PRICE_MONITOR_SUBSCRIPTION_RENOTIFICATION_MINUTES', 60 * 24 * 7)
# the email sender for notification emails
PRICE_MONITOR_EMAIL_SENDER = getattr(settings, 'PRICE_MONITOR_EMAIL_SENDER', 'noreply@localhost')
# default currency
PRICE_MONITOR_DEFAULT_CURRENCY = getattr(settings, 'PRICE_MONITOR_DEFAULT_CURRENCY', 'EUR')
# i18n for email notifications
PRICE_MONITOR_I18N_EMAIL_NOTIFICATION_SUBJECT = getattr(
    settings,
    'PRICE_MONITOR_I18N_EMAIL_NOTIFICATION_SUBJECT',
    ugettext_lazy('Price limit for %(product)s reached')
)
PRICE_MONITOR_I18N_EMAIL_NOTIFICATION_BODY = getattr(
    settings,
    'PRICE_MONITOR_I18N_EMAIL_NOTIFICATION_BODY',
    ugettext_lazy(
        'The price limit of %(price_limit)0.2f %(currency)s has been reached for the article "%(product_title)s" - '
        'the current price is %(price)0.2f %(currency)s.'
        '\n\nPlease support our platform by using this link for buying: %(link)s\n\n\nRegards,\nThe Team'
    )
)
PRICE_MONITOR_SITENAME = getattr(settings, 'PRICE_MONITOR_SITENAME', 'Price Monitor')

# cache settings
# key of cache (according to project config) to use for graphs. Set to none to disable caching
PRICE_MONITOR_GRAPH_CACHE_NAME = getattr(settings, 'PRICE_MONITOR_GRAPH_CACHE_NAME', None)
# prefix for cache key used for graphs
PRICE_MONITOR_GRAPH_CACHE_KEY_PREFIX = getattr(settings, 'PRICE_MONITOR_GRAPH_CACHE_KEY_PREFIX', 'graph_')


# internal settings - not to be overwritten by user
# Regex for ASIN validation
PRICE_MONITOR_ASIN_REGEX = r'[A-Z0-9\-]+'
# Product Advertising API relevant settings
# TODO is there a possibility to only get get attributes we need? I have the feeling that 75% of the data is irrelevant for us.
PRICE_MONITOR_PA_RESPONSE_GROUP = 'Large'
# mapping of PRICE_MONITOR_AMAZON_PRODUCT_API_REGION to the appropriate amazon domain ending
PRICE_MONITOR_AMAZON_REGION_DOMAINS = {
    'CA': 'ca',
    'DE': 'de',
    'ES': 'es',
    'FR': 'fr',
    'IN': 'in',
    'IT': 'it',
    'JP': 'co.jp',
    'UK': 'co.uk',
    'US': 'com',
}
PRICE_MONITOR_OFFER_URL = 'http://www.amazon.{domain:s}/dp/{asin:s}/?tag={assoc_tag:s}'
