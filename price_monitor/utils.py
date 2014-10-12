import warnings

from django.core.mail import send_mail as django_send_mail
from django.utils.translation import ugettext as _

from price_monitor import app_settings


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


def get_api():
    """
    Returns an AmazonAPI instance.
    :return: api instance
    :rtype: amazon.api.AmazonAPI
    """
    warnings.warn('get_api() is deprecated. Please use new structure!', DeprecationWarning, stacklevel=2)
    from amazon.api import AmazonAPI
    return AmazonAPI(
        app_settings.PRICE_MONITOR_AWS_ACCESS_KEY_ID,
        app_settings.PRICE_MONITOR_AWS_SECRET_ACCESS_KEY,
        app_settings.PRICE_MONITOR_AMAZON_PRODUCT_API_ASSOC_TAG,
        region=app_settings.PRICE_MONITOR_AMAZON_PRODUCT_API_REGION,
    )


def send_mail(title, price_limit, currency, price, offer_url, send_to):
    """
    Sends an email using the appropriate settings for formatting aso.
    :param title: title of the product
    :type title: str
    :param price_limit: the price limit set by the user
    :type price_limit: float
    :param currency: the used currency
    :type currency: string
    :param price: the current product price
    :type price: float
    :param offer_url: the offer url for the user to click
    :type offer_url: string
    :param send_to: the email address to send the email to
    :type send_to: str
    """
    django_send_mail(
        _(app_settings.PRICE_MONITOR_I18N_EMAIL_NOTIFICATION_SUBJECT) % {'product': title},
        _(app_settings.PRICE_MONITOR_I18N_EMAIL_NOTIFICATION_BODY) % {
            'price_limit': price_limit,
            'currency': currency,
            'price': price,
            'product_title': title,
            'link': offer_url,
        },
        app_settings.PRICE_MONITOR_EMAIL_SENDER,
        [send_to],
        fail_silently=False,
    )
