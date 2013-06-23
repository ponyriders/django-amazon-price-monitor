from django.conf import settings


# TODO prepend with "PRICE_MONITOR_"
AWS_ACCESS_KEY_ID = getattr(settings, 'AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = getattr(settings, 'AWS_SECRET_ACCESS_KEY', '')
AMAZON_PRODUCT_API_REGION = getattr(settings, 'AMAZON_PRODUCT_API_REGION', '')
AMAZON_PRODUCT_API_ASSOC_TAG = getattr(settings, 'AMAZON_PRODUCT_API_ASSOC_TAG', '')

# run product synchronization every X minutes
PRICE_MONITOR_PRODUCT_SYNCHRONIZE_TASK_RUN_EVERY_MINUTES = getattr(settings, 'PRICE_MONITOR_PRODUCT_SYNCHRONIZE_TASK_RUN_EVERY_MINUTES', 5)
# number of products to throw at once against the Amazon API
AMAZON_PRODUCT_SYNCHRONIZE_COUNT = getattr(settings, 'AMAZON_PRODUCT_SYNCHRONIZE_COUNT', 20)
# refresh product after 12 hours
AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES = getattr(settings, 'AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES', 12 * 60)
# time after when to notify about a subscription again
SUBSCRIPTION_RENOTIFICATION_MINUTES = getattr(settings, 'SUBSCRIPTION_RENOTIFICATION_MINUTES', 60 * 24 * 7)
# the email sender for notification emails
PRICE_MONITOR_EMAIL_SENDER = getattr(settings, 'PRICE_MONITOR_EMAIL_SENDER', 'noreply@localhost')