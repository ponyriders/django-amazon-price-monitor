import logging
import re

from django.core.mail import send_mail as django_send_mail
from django.utils.translation import ugettext as _

from price_monitor import app_settings


logger = logging.getLogger('price_monitor.utils')


def get_offer_url(asin):
    """
    Returns the offer url for an ASIN.
    :param asin: the asin
    :type asin: basestring
    :return: the url to the offer
    :rtype: basestring
    """
    return app_settings.PRICE_MONITOR_OFFER_URL.format(**{
        'domain': app_settings.PRICE_MONITOR_AMAZON_REGION_DOMAINS[app_settings.PRICE_MONITOR_AMAZON_PRODUCT_API_REGION],
        'asin': asin,
        'assoc_tag': app_settings.PRICE_MONITOR_AMAZON_PRODUCT_API_ASSOC_TAG,
    })


def parse_audience_rating(rating):
    """
    Parses the audience rating to a locale unaware value.
    :param rating: the localized rating string
    :type rating: basestring
    :return: rating as unified age
    :rtype: basestring
    """
    # FIXME this may fallback to default values if no value was returned by amazon?

    # FIXME this regex only handles currently known german values, see #19
    regex = re.compile('Freigegeben ab ([0-9]{1,2}) Jahren')
    result = regex.search(rating)

    if result is None:
        # regex won't match that
        if rating == 'Freigegeben ohne Altersbeschränkung':
            return 0

        logger.error('Unable to parse audience rating value "%(audience_rating)s"' % {'audience_rating': rating})
        return rating

    return int(result.groups()[0])


def send_mail(product, subscription, price):
    """
    Sends an email using the appropriate settings for formatting aso.
    :param product: the product
    :type product: price_monitor.models.Product
    :param subscription: the subscription
    :type subscription: price_monitor.models.Subscription
    :param price: the current price
    :type price: price_monitor.models.Price
    """
    django_send_mail(
        _(app_settings.PRICE_MONITOR_I18N_EMAIL_NOTIFICATION_SUBJECT) % {'product': product.title},
        _(app_settings.PRICE_MONITOR_I18N_EMAIL_NOTIFICATION_BODY) % {
            'price_limit': subscription.price_limit,
            'currency': price.currency,
            'price': price.value,
            'product_title': product.title,
            'link': product.offer_url,
        },
        app_settings.PRICE_MONITOR_EMAIL_SENDER,
        [subscription.email_notification.email],
        fail_silently=False,
    )


def chunk_list(the_list, chunk_size):
    """
    Chunks a list.
    :param the_list: list to chunk
    :type the_list: list
    :param chunk_size: number of elements to be contained in each created chunk list
    :type chunk_size: int
    :return: generator object with the chunked lists
    :rtype: generator
    """
    for i in range(0, len(the_list), chunk_size):
        yield the_list[i:i + chunk_size]
