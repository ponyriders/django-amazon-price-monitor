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
        self.__amazon = bottlenose.Amazon(
            AWSAccessKeyId=app_settings.PRICE_MONITOR_AWS_ACCESS_KEY_ID,
            AWSSecretAccessKey=app_settings.PRICE_MONITOR_AWS_SECRET_ACCESS_KEY,
            AssociateTag=app_settings.PRICE_MONITOR_AMAZON_PRODUCT_API_ASSOC_TAG,
            Region=app_settings.PRICE_MONITOR_AMAZON_PRODUCT_API_REGION,
            Parser=BeautifulSoup,
            ErrorHandler=ProductAdvertisingAPI.handle_error,
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

    @staticmethod
    def handle_error(error):
        """
        Generic error handler for bottlenose requests.
        @see https://github.com/lionheart/bottlenose#error-handling
        :param error: error information
        :type error: dict
        :return: if to retry the request
        :rtype: bool
        :
        """
        logger.error(
            'Error was thrown upon requesting URL %(api_url)s (Cache-URL: %(cache_url)s: %(exception)r' % {
                'api_url': error['api_url'],
                'cache_url': error['cache_url'],
                'exception': error['exception'],
            }
        )
        # FIXME we do not retry failed requests for now
        return False

    def item_lookup(self, item_id):
        """
        Lookup of the item with the given id on Amazon. Returns it values or None if something went wrong.
        :param item_id: the item id
        :type item_id: basestring
        :return: the values of the item
        :rtype: dict
        """
        item_response = self.__amazon.ItemLookup(ItemId=item_id, ResponseGroup=app_settings.PRICE_MONITOR_PA_RESPONSE_GROUP)
        if item_response.items.request.isvalid.string == 'True':
            item_node = item_response.items.item
            if item_node is not None:
                # TODO may cause value conversion errors, if so, encapsulate with specific exception handling
                # FIXME maybe we could put that into an intermediate class that handles the value conversions itself
                return {
                    'asin': item_node.asin.string,
                    'title': item_node.itemattributes.title.string,
                    'isbn': self.__get_item_attribute(item_node, 'isbn'),
                    'eisbn': self.__get_item_attribute(item_node, 'eisbn'),
                    'binding': item_node.itemattributes.binding.string,
                    'date_publication': datetime.strptime(self.__get_item_attribute(item_node, 'publicationdate'), '%Y-%m-%d'),
                    'date_release': datetime.strptime(self.__get_item_attribute(item_node, 'releasedate'), '%Y-%m-%d'),
                    'audience_rating': utils.parse_audience_rating(self.__get_item_attribute(item_node, 'audiencerating')),
                    'large_image_url': item_node.largeimage.url.string,
                    'medium_image_url': item_node.mediumimage.url.string,
                    'small_image_url': item_node.smallimage.url.string,
                    'offer_url': utils.get_offer_url(item_node.asin.string),
                }
            else:
                logger.error('Lookup for item with ASIN %(item_id)s returned no product' % {'item_id': item_id})
                return None
        else:
            logger.error(
                'Request for item lookup (ResponseGroup: %(response_group)s, ASIN: %(item_id)s) was not vaild' % {
                    'response_group': app_settings.PRICE_MONITOR_PA_RESPONSE_GROUP,
                    'item_id': item_id,
                }
            )
            return None
