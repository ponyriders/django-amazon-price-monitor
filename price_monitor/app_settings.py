from django.conf import settings


AWS_ACCESS_KEY_ID = getattr(settings, 'AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = getattr(settings, 'AWS_SECRET_ACCESS_KEY', '')
AMAZON_PRODUCT_API_REGION = getattr(settings, 'AMAZON_PRODUCT_API_REGION', '')
AMAZON_PRODUCT_API_ASSOC_TAG = getattr(settings, 'AMAZON_PRODUCT_API_ASSOC_TAG', '')

# run product synchronization every X minutes
PRICE_MONITOR_PRODUCTS_SYNCHRONIZE_TASK_RUN_EVERY_MINUTES = getattr(settings, 'PRICE_MONITOR_PRODUCTS_SYNCHRONIZE_TASK_RUN_EVERY_MINUTES', 5)
# number of products to throw against the Amazon API at once, limited by Amazon to a maximum of 10, see bug #17
TMP_SYNC_COUNT = getattr(settings, 'PRICE_MONITOR_AMAZON_PRODUCT_SYNCHRONIZE_COUNT', 10)
PRICE_MONITOR_AMAZON_PRODUCT_SYNCHRONIZE_COUNT = 10 if TMP_SYNC_COUNT > 10 else TMP_SYNC_COUNT
# refresh product after 12 hours
PRICE_MONITOR_AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES = getattr(settings, 'PRICE_MONITOR_AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES', 12 * 60)
# time after when to notify about a subscription again
PRICE_MONITOR_SUBSCRIPTION_RENOTIFICATION_MINUTES = getattr(settings, 'PRICE_MONITOR_SUBSCRIPTION_RENOTIFICATION_MINUTES', 60 * 24 * 7)
# the email sender for notification emails
PRICE_MONITOR_EMAIL_SENDER = getattr(settings, 'PRICE_MONITOR_EMAIL_SENDER', 'noreply@localhost')

# i18n for email notifications
gettext = lambda x: x
PRICE_MONITOR_I18N_EMAIL_NOTIFICATION_SUBJECT = gettext('Price limit for %(product)s reached')
PRICE_MONITOR_I18N_EMAIL_NOTIFICATION_BODY = gettext(
    'The price limit of %(price_limit)0.2f %(currency)s has been reached for the article "%(product_title)s" - the current price is %(price)0.2f %(currency)s.'
    '\n\nPlease support our platform by using this link for buying: %(link)s\n\n\nRegards,\nThe Team'
)
PRICE_MONITOR_SITENAME = getattr(settings, 'PRICE_MONITOR_SITENAME', 'Price Monitor')

# Regex for ASIN validation
PRICE_MONITOR_ASIN_REGEX = getattr(settings, 'PRICE_MONITOR_ASIN_REGEX', r'[A-Z0-9\-]+')

# serve the product images via HTTPS
PRICE_MONITOR_IMAGES_USE_SSL = getattr(settings, 'PRICE_MONITOR_IMAGES_USE_SSL', True)
# HTTPS host to use for getting the images. Seems to be https://images-<REGION>.ssl-images-amazon.com.
PRICE_MONITOR_AMAZON_SSL_IMAGE_DOMAIN = getattr(settings, 'PRICE_MONITOR_AMAZON_SSL_IMAGE_DOMAIN', 'https://images-eu.ssl-images-amazon.com')
