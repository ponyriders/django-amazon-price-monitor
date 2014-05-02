import logging

from . import app_settings as settings
from .api import get_api
from amazon.api import (
    AmazonProduct,
    AsinNotFound,
    LookupException,
)
from celery.task import PeriodicTask, Task
from django.core.mail import send_mail
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext as _
from datetime import timedelta
from itertools import islice
from price_monitor.models import (
    Price,
    Product,
    Subscription,
)
from smtplib import SMTPServerDisconnected


logger = logging.getLogger('price_monitor')


class ProductSynchronizationMixin(object):
    """
    Mixin encapsulating the functionality to update a product.
    Used by the tasks:
    - ProductsSynchronizeTask (Periodic)
    """

    @staticmethod
    def sync_product(amazon_product, product):
        """
        Synchronizes the given price_monitor.model.Product with the Amazon lookup product.
        :param amazon_product: the Amazon product
        :type amazon_product: amazon.api.AmazonProduct
        :param product: the product to update
        :type product: price_monitor.models.Product
        """
        now = timezone.now()

        product.set_values_from_amazon_product(amazon_product)
        product.status = 1
        product.date_last_synced = now
        product.save()

        # tuple: (price, currency)
        price = amazon_product.price_and_currency

        if not price[0] is None:
            # get all subscriptions of product that are subscribed to the current price or a higher one and
            # whose owners have not been notified about that particular subscription price since before
            # settings.PRICE_MONITOR_SUBSCRIPTION_RENOTIFICATION_MINUTES.
            for sub in Subscription.objects.filter(
                Q(
                    product=product,
                    price_limit__gte=price[0],
                    date_last_notification__lte=(timezone.now() - timedelta(minutes=settings.PRICE_MONITOR_SUBSCRIPTION_RENOTIFICATION_MINUTES))
                ) | Q(
                    product=product,
                    price_limit__gte=price[0],
                    date_last_notification__isnull=True
                )
            ):
                # TODO: how to handle failed notifications?
                NotifySubscriberTask().delay(product, price[0], price[1], sub)

            # create the price entry
            Price.objects.create(
                value=price[0],
                currency=price[1],
                date_seen=now,
                product=product,
            )

    @staticmethod
    def get_products_to_sync():
        """
        Returns the products to synchronize.
        These are newly created products with status "0" or products that are older than settings.PRICE_MONITOR_AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES.
        :return: tuple with 0: dictionary with the Products and 1: if there are still products that need to be synced
        :rtype: tuple
        """
        # prefer already synced products over newly created
        products = {
            p.asin: p for p in Product.objects.select_related().filter(
                subscription__isnull=False,
                date_last_synced__lte=(timezone.now() - timedelta(minutes=settings.PRICE_MONITOR_AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES))
            )
        }

        # there is still some space for products to sync, append newly created if available
        if len(products) < settings.PRICE_MONITOR_AMAZON_PRODUCT_SYNCHRONIZE_COUNT:
            return (
                dict(
                    list(products.items()) + list({
                        p.asin: p for p in Product.objects.select_related().filter(status=0)
                            .order_by('date_creation')[:(settings.PRICE_MONITOR_AMAZON_PRODUCT_SYNCHRONIZE_COUNT - len(products))]
                    }.items())
                ),
                # set recall to true if there are more unsynched products than already included
                Product.objects.select_related().filter(status=0).count() > settings.PRICE_MONITOR_AMAZON_PRODUCT_SYNCHRONIZE_COUNT - len(products)
            )
        else:
            def take(n, iterable):
                """
                Takes n elements out of the given iterable.
                :param n: number of elements to take
                :type n: int
                :param iterable; the iterable dict
                :type iterable: dictionary-itemiterator
                :returns: the resized dictionary
                :rtype : dict
                """
                return dict(list(islice(iterable, n)))

            return take(settings.PRICE_MONITOR_AMAZON_PRODUCT_SYNCHRONIZE_COUNT, iter(products.items())), True


class ProductsSynchronizeTask(PeriodicTask, ProductSynchronizationMixin):
    """
    Synchronizes Products in status "Created" (0) initially with Product API.
    """
    run_every = timedelta(minutes=settings.PRICE_MONITOR_PRODUCTS_SYNCHRONIZE_TASK_RUN_EVERY_MINUTES)

    def run(self, **kwargs):
        """
        Runs the synchronization by fetching settings.PRICE_MONITOR_AMAZON_PRODUCT_SYNCHRONIZE_COUNT number of products and requests their data from Amazon.
        """
        products, recall = self.get_products_to_sync()

        # exit if there is no food
        if len(products) == 0:
            logger.info('No products to sync.')
            return
        else:
            logger.info(
                'Syncing %(count)d products. %(recall)s' % {
                    'count': len(products),
                    'recall': 'Still more products available to sync.' if recall else 'No more products to sync there.'
                }
            )

        try:
            lookup = get_api().lookup(ItemId=','.join(list(products.keys())))
        except (LookupException, AsinNotFound):
            # if the lookup for all ASINs fails, do one by one to get the erroneous one(s)
            for asin, product in list(products.items()):
                try:
                    lookup = get_api().lookup(ItemId=asin)
                except (LookupException, AsinNotFound):
                    logger.exception('unable to lookup product with asin %s' % asin)
                    product.set_failed_to_sync()
                else:
                    self.sync_product(lookup, product)
        except UnicodeEncodeError:
            logger.exception('Unable to communicate with Amazon, the access key is probably not allowed to fetch Product API.')
        else:
            # api.lookup hides a list of AmazonProducts or a single AmazonProduct
            if type(lookup) == AmazonProduct:
                lookup = [lookup]

            # iterate an sync
            for amazon_product in lookup:
                self.sync_product(amazon_product, products[amazon_product.asin])

            # finally, if there are more products that can be synchronized, recall the task
            if recall:
                self.apply_async(countdown=120)


class ProductSynchronizeTask(Task, ProductSynchronizationMixin):
    """
    Task for synchronizing a single product.
    """

    def run(self, product, **kwargs):
        """
        Queries the API with the ASIN of the given product and synchronizes the fields.
        :param product: the base Product to use
        :type product: price_monitor.model.Product
        """
        logger.info('synchronizing Product with ASIN %(asin)s' % {'asin': product.asin})

        try:
            lookup = get_api().lookup(ItemId=product.asin)
        except (LookupException, AsinNotFound):
            logger.exception('Unable to synchronize product with ASIN %(asin)s' % {'asin': product.asin})
            product.set_failed_to_sync()
        except UnicodeEncodeError:
            logger.exception('Unable to communicate with Amazon, the access key is probably not allowed to fetch Product API.')
        else:
            self.sync_product(lookup, product)


class NotifySubscriberTask(Task):
    """
    Task for notifying a single user about a product that has reached the desired price.
    """

    def run(self, product, price, currency, subscription, **kwargs):
        """
        Sends an email to the subscriber.
        :param product: the product to notify about
        :param price: the current price of the product
        :param currency:  the currency of the price
        :param subscription: the Subscription class connecting subscriber and product
        :type product: .Product
        :type price: float
        :type currency: string
        :type subscription: .Subscription
        """
        logger.info('Trying to send notification email to %(email)s...' % {'email': subscription.email_notification.email})
        try:
            send_mail(
                _(settings.PRICE_MONITOR_I18N_EMAIL_NOTIFICATION_SUBJECT) % {'product': product.title},
                _(settings.PRICE_MONITOR_I18N_EMAIL_NOTIFICATION_BODY) % {
                    'price_limit': subscription.price_limit,
                    'currency': currency,
                    'price': price,
                    'product_title': product.title,
                    'link': product.offer_url,
                },
                settings.PRICE_MONITOR_EMAIL_SENDER,
                [subscription.email_notification.email],
                fail_silently=False,
            )
        except SMTPServerDisconnected:
            logger.exception('SMTP server was disconnected.')
        else:
            logger.info('Notification email to %(email)s was sent!' % {'email': subscription.email_notification.email})
            subscription.date_last_notification = timezone.now()
            subscription.save()
