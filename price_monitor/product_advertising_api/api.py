import bottlenose
import logging

from bs4 import BeautifulSoup

from price_monitor import app_settings


logger = logging.getLogger('price_monitor.product_advertising_api')


# TODO reshape all models to the values we need, then do the parsing of ItemLookup


class ProductAdvertisingAPI(object):
    """
    A wrapper class for the necessary Amazon Product Advertising API calls.
    See the API reference here: http://docs.aws.amazon.com/AWSECommerceService/latest/DG/CHAP_ApiReference.html
    See bottlenose here: https://github.com/lionheart/bottlenose
    """

    def __init__(self):
        # FIXME needs some more code?
        # TODO use Caching https://github.com/lionheart/bottlenose#caching
        # TODO use ErrorHandling https://github.com/lionheart/bottlenose#error-handling
        self.__amazon = bottlenose.Amazon(
            AWSAccessKeyId=app_settings.PRICE_MONITOR_AWS_ACCESS_KEY_ID,
            AWSSecretAccessKey=app_settings.PRICE_MONITOR_AWS_SECRET_ACCESS_KEY,
            AssociateTag=app_settings.PRICE_MONITOR_AMAZON_PRODUCT_API_ASSOC_TAG,
            Region=app_settings.PRICE_MONITOR_AMAZON_PRODUCT_API_REGION,
            Parser=BeautifulSoup,
        )

    def item_lookup(self, item_id):
        item = self.__amazon.ItemLookup(ItemId=item_id, ResponseGroup=app_settings.PRICE_MONITOR_PA_RESPONSE_GROUP)
        # TODO get what we need and extract these generic functionality
