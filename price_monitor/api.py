from amazon.api import AmazonAPI
from . import app_settings as settings


def get_api():
    """
    Returns an AmazonAPI instance.
    :return: api instance
    :rtype: amazon.api.AmazonAPI
    """
    return AmazonAPI(
        settings.AWS_ACCESS_KEY_ID,
        settings.AWS_SECRET_ACCESS_KEY,
        settings.AMAZON_PRODUCT_API_ASSOC_TAG,
        region=settings.AMAZON_PRODUCT_API_REGION,
    )
