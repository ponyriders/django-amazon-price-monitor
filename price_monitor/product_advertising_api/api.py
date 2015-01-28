import bottlenose
import logging

from bs4 import BeautifulSoup

from datetime import datetime

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

    @staticmethod
    def __get_item_attribute(item, attribute):
        """
        Returns the attribute value from a bs4 parsed item.
        :param item: bs4 item returned from PA API upon item lookup
        :param attribute: the attribute to search for
        :return: the value if found, else None
        :rtype: basestring
        """
        value = item.itemattributes.find_all(attribute, recursive=False)
        return value[0].string if len(value) == 1 else None

    def item_lookup(self, item_id):
        item_response = self.__amazon.ItemLookup(ItemId=item_id, ResponseGroup=app_settings.PRICE_MONITOR_PA_RESPONSE_GROUP)
        if item_response.items.request.isvalid.string == 'True':
            item_node = item_response.items.item
            if item_node is not None:
                item_values = {
                    'asin': item_node.asin.string,
                    'title': item_node.itemattributes.title.string,
                    'isbn': self.__get_item_attribute(item_node, 'isbn'),
                    'eisbn': self.__get_item_attribute(item_node, 'eisbn'),
                    'binding': item_node.itemattributes.binding.string,
                    'date_publication': datetime.strptime(self.__get_item_attribute(item_node, 'publicationdate'), '%Y-%m-%d'),
                    'date_release': datetime.strptime(self.__get_item_attribute(item_node, 'releasedate'), '%Y-%m-%d'),
                    # TODO collect possible values and parse them? see #19
                    'audience_rating': self.__get_item_attribute(item_node, 'audiencerating'),
                    'large_image_url': item_node.largeimage.url.string,
                    'medium_image_url': item_node.mediumimage.url.string,
                    'small_image_url': item_node.smallimage.url.string,
                    'offer_url': utils.get_offer_url(item_node.asin.string),
                }
                print(item_values)
            else:
                # FIXME was unable to find item
                return None
        else:
            # FIXME request was invalid
            return None
