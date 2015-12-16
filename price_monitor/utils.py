"""Several util functions"""
import logging

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


def get_product_detail_url(asin):
    """
    Returns the url to a product detail view.

    As the frontend is AngularJS, we cannot use any Django reverse functionality.
    :param asin: the asin to use
    :return: the link
    """
    return '{base_url:s}/#/products/{asin:s}'.format(
        base_url=app_settings.PRICE_MONITOR_BASE_URL,
        asin=asin,
    )


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
        _(app_settings.PRICE_MONITOR_I18N_EMAIL_NOTIFICATION_BODY).format(
            price_limit=subscription.price_limit,
            currency=price.currency,
            price=price.value,
            product_title=product.get_title(),
            url_product_amazon=product.offer_url,
            url_product_detail=get_product_detail_url(product.asin),
        ),
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
