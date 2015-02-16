import logging

from celery.task import Task

from datetime import timedelta

from django.utils import timezone

from itertools import islice

from price_monitor import app_settings
from price_monitor.models import (
    Price,
    Product,
)
from price_monitor.product_advertising_api.api import ProductAdvertisingAPI


logger = logging.getLogger('price_monitor')


class SynchronizationMixin():

    @staticmethod
    def sync_product(product, amazon_data):
        """
        Synchronizes the given price_monitor.model.Product with the Amazon data.
        :param product: the product to update
        :type product: price_monitor.models.Product
        :param amazon_data: the date from the amazon api
        :type amazon_data: dict
        """
        now = timezone.now()

        # create the price
        price = Price.objects.create(
            value=amazon_data['price'],
            currency=amazon_data['currency'],
            date_seen=now,
            product=product,
        )

        # remove the elements that are not a field in Product model
        amazon_data.pop('price')
        amazon_data.pop('currency')

        # update and save the product
        product.__dict__.update(amazon_data)
        product.status = 1
        product.date_last_synced = now
        product.save()

        # FIXME adjust price handling
        # # tuple: (price, currency)
        # price = amazon_product.price_and_currency
        #
        # if not price[0] is None:
        #     # get all subscriptions of product that are subscribed to the current price or a higher one and
        #     # whose owners have not been notified about that particular subscription price since before
        #     # settings.PRICE_MONITOR_SUBSCRIPTION_RENOTIFICATION_MINUTES.
        #     for sub in Subscription.objects.filter(
        #         Q(
        #             product=product,
        #             price_limit__gte=price[0],
        #             date_last_notification__lte=(timezone.now() - timedelta(minutes=settings.PRICE_MONITOR_SUBSCRIPTION_RENOTIFICATION_MINUTES))
        #         ) | Q(
        #             product=product,
        #             price_limit__gte=price[0],
        #             date_last_notification__isnull=True
        #         )
        #     ):
        #         # TODO: how to handle failed notifications?
        #         NotifySubscriberTask().delay(product, price[0], price[1], sub)

    def get_products_to_sync(self):
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
                date_last_synced__lte=(timezone.now() - timedelta(minutes=app_settings.PRICE_MONITOR_AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES)),
                # issue #21 don't sync products that are  not existent
                status__in=[0, 1]
            )
        }

        # there is still some space for products to sync, append newly created if available
        if len(products) < app_settings.PRICE_MONITOR_AMAZON_PRODUCT_SYNCHRONIZE_COUNT:
            return (
                dict(
                    list(products.items()) + list(
                        {
                            p.asin: p for p in Product.objects.select_related().filter(status=0).order_by('date_creation')[
                                :(app_settings.PRICE_MONITOR_AMAZON_PRODUCT_SYNCHRONIZE_COUNT - len(products))
                            ]
                        }.items()
                    )
                ),
                # set recall to true if there are more unsynched products than already included
                Product.objects.select_related().filter(status=0).count() > app_settings.PRICE_MONITOR_AMAZON_PRODUCT_SYNCHRONIZE_COUNT - len(products)
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

            return take(app_settings.PRICE_MONITOR_AMAZON_PRODUCT_SYNCHRONIZE_COUNT, iter(products.items())), True


class SynchronizeSingleProductTask(Task, SynchronizationMixin):
    """
    Task for synchronizing a single product.
    """

    def run(self, item_id):
        """
        Called by celery if task is being delayed.
        :param item_id: the ItemId that uniquely identifies a product
        :type  item_id: basestring
        """
        logger.info('Synchronizing Product with ItemId %(item_id)s' % {'item_id': item_id})

        try:
            product = Product.objects.get(asin=item_id)
        except Product.DoesNotExist:
            logger.exception('Product with ASIN %(item_id)s does not exist - unable to synchronize with API.' % {'item_id': item_id})

        self.sync_product(product, ProductAdvertisingAPI().item_lookup(item_id=item_id))
