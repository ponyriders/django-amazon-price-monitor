import logging

from celery import chord
from celery.signals import celeryd_after_setup
from celery.task import Task

from datetime import timedelta

from django.db.models import (
    Min,
    Q,
)
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


logger = logging.getLogger('price_monitor.product_advertising_api')


@celeryd_after_setup.connect
def celeryd_after_setup(*args, **kwargs):
    """
    Called after the worker instances are set up.
    Starts the StartupTask to get the whole synchronization started.
    """
    StartupTask().apply_async(countdown=5)


class StartupTask(Task):
    """
    The task for getting the machinery up and running. As we do not use celery beat, we have to start somewhere.
    """
    ignore_result = True

    def run(self):
        logger.info('StartupTask was called')
        # 5 seconds after startup we start the synchronization
        FindProductsToSynchronizeTask().apply_async(countdown=5)


# FIXME this task should only be enqueued ONCE. so if there is already a task queued, it shall not be queued additionally.
class FindProductsToSynchronizeTask(Task):
    """
    The tasks that finds the products that shall be updated through the api.
    """
    def run(self):
        """
        Fetches the products to update via api. Queues a single SynchronizeSingleProductTask for each product and calls a new instance of itself after all
        tasks are done. If no products found for update, sleeps until the next update time is reached.
        :return: the result is always true
        :rtype: bool
        """
        logger.info('FindProductsToSynchronizeTask was called')

        # get all products that shall be updated
        products = self.__get_products_to_sync()

        if len(products) > 0:
            logger.info('Starting chord for synchronization of %d products', len(products))
            # after all single product synchronize tasks are done recall the FindProductsToSynchronizeTask. That is because we do not know how long it takes to
            # synchronize the products and there can be new ones meanwhile. If the newly called task finds no products, it will handle the new callback to the
            # correct time.
            chord(
                SynchronizeSingleProductTask().s(product) for product in products
            )(
                FindProductsToSynchronizeTask().si()
            )
        else:
            logger.info('No products found to update now')
            # One might think this may interfere with newly created products and their synchronization if they are added before the
            # FindProductsToSynchronizeTask is called again, but it doesn't. The new product is updated on creation and the next synchronization is always
            # after the next task call.
            oldest_synchronization = Product.objects.filter(subscription__isnull=False, status__in=[0, 1]).aggregate(
                Min('date_last_synced')
            )['date_last_synced__min']
            next_synchronization = oldest_synchronization + timedelta(minutes=app_settings.PRICE_MONITOR_AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES)
            logger.info('Eta for next FindProductsToSynchronizeTask run is %s', next_synchronization)
            FindProductsToSynchronizeTask().apply_async(eta=next_synchronization)

        return True

    def __get_products_to_sync(self):
        """
        Returns the products to synchronize.
        These are newly created products with status "0" or products that are older than settings.PRICE_MONITOR_AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES.
        :return: list of products
        :rtype: django.db.models.query.QuerySet
        """
        # prefer already synced products over newly created
        return Product.objects.select_related().filter(
            subscription__isnull=False,
            date_last_synced__lte=(timezone.now() - timedelta(minutes=app_settings.PRICE_MONITOR_AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES)),
            # issue #21 don't sync products that are  not existent
            status__in=[0, 1]
        )


class SynchronizeSingleProductTask(Task):
    """
    Task for synchronizing a single product.
    """
    # limit to one task per second, limited by Amazon API
    rate_limit = '1/s'

    def run(self, product):
        """
        Called by celery if task is being delayed.
        :param product: the product to sycnhronize with amazon
        :type  product: price_monitor.models.Product
        """
        logger.info('Synchronizing Product with ItemId %(item_id)s' % {'item_id': product.asin})
        self.__sync_product(product, ProductAdvertisingAPI().item_lookup(item_id=product.asin))
        return True

    def __sync_product(self, product, amazon_data):
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
                # FIXME: how to handle failed notifications?
                NotifySubscriberTask().apply_async((product, price, sub), countdown=1)


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
