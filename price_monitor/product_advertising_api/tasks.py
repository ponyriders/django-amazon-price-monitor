import logging

from celery.task import (
    Task,
    PeriodicTask,
)

from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from price_monitor import app_settings
from price_monitor.models import (
    Price,
    Product,
    Subscription,
)
from price_monitor.product_advertising_api.api import ProductAdvertisingAPI
from price_monitor.utils import send_mail

from smtplib import SMTPServerDisconnected


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
        price = None
        if 'price' in amazon_data:
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

        if price is not None:
            # get all subscriptions of product that are subscribed to the current price or a higher one and
            # whose owners have not been notified about that particular subscription price since before
            # settings.PRICE_MONITOR_SUBSCRIPTION_RENOTIFICATION_MINUTES.
            for sub in Subscription.objects.filter(
                Q(
                    product=product,
                    price_limit__gte=price.value,
                    date_last_notification__lte=(timezone.now() - timedelta(minutes=app_settings.PRICE_MONITOR_SUBSCRIPTION_RENOTIFICATION_MINUTES))
                ) | Q(
                    product=product,
                    price_limit__gte=price.value,
                    date_last_notification__isnull=True
                )
            ):
                # TODO: how to handle failed notifications?
                NotifySubscriberTask().apply_async((product, price, sub), countdown=1)

    def get_products_to_sync(self):
        """
        Returns the products to synchronize.
        These are newly created products with status "0" or products that are older than settings.PRICE_MONITOR_AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES.
        :return: tuple with 0: dictionary with the Products and 1: if there are still products that need to be synced
        :rtype: tuple
        """
        # prefer already synced products over newly created
        products = list(
            Product.objects.select_related().filter(
                subscription__isnull=False,
                date_last_synced__lte=(timezone.now() - timedelta(minutes=app_settings.PRICE_MONITOR_AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES)),
                # issue #21 don't sync products that are  not existent
                status__in=[0, 1]
            )
        )

        # there is still some space for products to sync, append newly created if available
        if len(products) < app_settings.PRICE_MONITOR_AMAZON_PRODUCT_SYNCHRONIZE_COUNT:
            # number of products that can be added
            remaining_product_places = app_settings.PRICE_MONITOR_AMAZON_PRODUCT_SYNCHRONIZE_COUNT - len(products)

            return (
                products + list(Product.objects.select_related().filter(status=0).order_by('date_creation')[:remaining_product_places]),
                # set recall to true if there are more unsynchronized products than already included
                Product.objects.select_related().filter(status=0).count() > app_settings.PRICE_MONITOR_AMAZON_PRODUCT_SYNCHRONIZE_COUNT - len(products),
            )
        else:
            return products[:app_settings.PRICE_MONITOR_AMAZON_PRODUCT_SYNCHRONIZE_COUNT], True


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
            return

        self.sync_product(product, ProductAdvertisingAPI().item_lookup(item_id=item_id))


class SynchronizeProductsPeriodicallyTask(PeriodicTask, SynchronizationMixin):
    """
    Task for periodically synchronizing of products.
    """
    run_every = timedelta(minutes=app_settings.PRICE_MONITOR_PRODUCTS_SYNCHRONIZE_TASK_RUN_EVERY_MINUTES)

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
                'Starting synchronization of %d products. %s',
                len(products),
                'Still more products available to sync.' if recall else 'No more products to sync there.'
            )

        for product in products:
            self.sync_product(product, ProductAdvertisingAPI().item_lookup(item_id=product.asin))

        # finally, if there are more products that can be synchronized, recall the task
        if recall:
            self.apply_async(countdown=5)


class NotifySubscriberTask(Task):
    """
    Task for notifying a single user about a product that has reached the desired price.
    """

    def run(self, product, price, subscription, **kwargs):
        """
        Sends an email to the subscriber.
        :param product: the product to notify about
        :type product: price_monitor.models.Product
        :param price: the current price of the product
        :type price: price_monitor.models.Price
        :param subscription: the Subscription class connecting subscriber and product
        :type subscription: price_monitor.models.Subscription
        """
        logger.info('Trying to send notification email to %(email)s...' % {'email': subscription.email_notification.email})
        try:
            send_mail(product, subscription, price)
        except SMTPServerDisconnected:
            logger.exception('SMTP server was disconnected.')
        else:
            logger.info('Notification email to %(email)s was sent!' % {'email': subscription.email_notification.email})
            subscription.date_last_notification = timezone.now()
            subscription.save()
