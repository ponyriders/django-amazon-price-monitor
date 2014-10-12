import bottlenose
import logging

from bs4 import BeautifulSoup

from price_monitor import (
    app_settings,
    utils,
)


logger = logging.getLogger('price_monitor.product_advertising_api')


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
        item_response = self.__amazon.ItemLookup(ItemId=item_id, ResponseGroup=app_settings.PRICE_MONITOR_PA_RESPONSE_GROUP)
        if item_response.items.request.isvalid.string == 'True':
            item_node = item_response.items.item
            # FIXME remove noga after implementing
            item_values = {  # noqa
                'asin': item_node.asin.string,
                'title': item_node.itemattributes.title.string,
                # FIXME find path, use 3832796096
                'isbn': None,
                # FIXME find path, use 3832796096
                'eisbn': None,
                'binding': item_node.itemattributes.binding.string,
                # FIXME find path, use ASIN B00JIR8U3U
                'date_publication': None,
                # FIXME this is YYYY-MM-DD
                'date_release': item_node.itemattributes.releasedate.string,
                # FIXME collect possible values and parse them? see #19
                'audience_rating': item_node.itemattributes.audiencerating.string,
                'large_image_url': item_node.largeimage.url.string,
                'medium_image_url': item_node.mediumimage.url.string,
                'small_image_url': item_node.smallimage.url.string,
                'offer_url': utils.get_offer_url(item_node.asin.string),
            }
        else:
            # FIXME handle the error
            pass
