from django.conf import settings


AWS_ACCESS_KEY_ID = getattr(settings, 'AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = getattr(settings, 'AWS_SECRET_ACCESS_KEY', '')
AMAZON_PRODUCT_API_REGION = getattr(settings, 'AMAZON_PRODUCT_API_REGION', '')
AMAZON_PRODUCT_API_ASSOC_TAG = getattr(settings, 'AMAZON_PRODUCT_API_ASSOC_TAG', '')

# number of products to throw at once against the Amazon API
AMAZON_PRODUCT_SYNCHRONIZE_COUNT = getattr(settings, 'AMAZON_PRODUCT_SYNCHRONIZE_COUNT', 20)
# refresh product after 12 hours
AMAZON_PRODUCT_REFRESH_THRESHOLD = getattr(settings, 'AMAZON_PRODUCT_REFRESH_THRESHOLD', 43200)