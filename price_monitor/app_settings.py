from django.conf import settings


AWS_ACCESS_KEY_ID = getattr(settings, 'AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = getattr(settings, 'AWS_SECRET_ACCESS_KEY', '')
AMAZON_PRODUCT_API_REGION = getattr(settings, 'AMAZON_PRODUCT_API_REGION', '')
AMAZON_PRODUCT_API_ASSOC_TAG = getattr(settings, 'AMAZON_PRODUCT_API_ASSOC_TAG', '')

PRODUCT_SYNCHRONIZE_COUNT = getattr(settings, 'PRODUCT_SYNCHRONIZE_COUNT', 10)
