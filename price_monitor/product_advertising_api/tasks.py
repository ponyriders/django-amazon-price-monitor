import logging

from celery import chord
from celery.signals import celeryd_after_setup
from celery.task import Task
from celery.task.control import inspect

from datetime import (
    datetime,
    timedelta,
)

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
from price_monitor.utils import (
    chunk_list,
    send_mail,
)

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

        # fetch all scheduled tasks
        scheduled_tasks = inspect().scheduled()

        # iterate the scheduled task values, see http://docs.celeryproject.org/en/latest/userguide/workers.html?highlight=revoke#dump-of-scheduled-eta-tasks
        for task_values in iter(scheduled_tasks.values()):
            # task_values is a list of dicts
            for task in task_values:
                if task['request']['name'] == '{}.{}'.format(FindProductsToSynchronizeTask.__module__, FindProductsToSynchronizeTask.__name__):
                    logger.info('FindProductsToSynchronizeTask is already scheduled, skipping additional run')
                    return

        # 5 seconds after startup we start the synchronization
        FindProductsToSynchronizeTask().apply_async(countdown=5)


class FindProductsToSynchronizeTask(Task):
    """
    The tasks that finds the products that shall be updated through the api.
    """
    def run(self):
        """
        Fetches the products to update via api. Queues a SynchronizeProductsTask and calls a new instance of itself after all
        tasks are done. If no products found for update, sleeps until the next update time is reached.
        :return: the result is always true
        :rtype: bool
        """
        logger.info('FindProductsToSynchronizeTask was called')

        # get all products that shall be updated
        products = self.__get_products_to_sync()

        if len(products) > 0:
            # chunk the products into 10 products each
            products_chunked = list(chunk_list(list(products), 10))

            logger.info('Starting chord for synchronization of %d products in %d chunks', len(products), len(products_chunked))

            # after all single product synchronize tasks are done recall the FindProductsToSynchronizeTask. That is because we do not know how long it takes to
            # synchronize the products and there can be new ones meanwhile. If the newly called task finds no products, it will handle the new callback to the
            # correct time.
            chord(
                SynchronizeProductsTask().s([product.asin for product in product_list]) for product_list in products_chunked
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
            )['date_last_synced__min'] or datetime.now()
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


class SynchronizeProductsTask(Task):
    """
    Task for synchronizing a single product.
    """
    # limit to one task per second, limited by Amazon API
    rate_limit = '1/s'

    # if we use the product instances instead of asins we get an EncodeError(RuntimeError('maximum recursion depth exceeded',),) resulting in a
    # billiard.exceptions.WorkerLostError:
    def run(self, asin_list):
        """
        Called by celery if task is being delayed.
        :param asin_list: list of asins of the products to be sycnhronized with Amazon
        :type  asin_list: list
        """
        products = dict()
        # fetch the product instances
        for asin in asin_list:
            try:
                # do select_related for price values for reducing db queries
                product = Product.objects.select_related('highest_price', 'lowest_price', 'current_price').get(asin=asin)
            except Product.DoesNotExist:
                logger.error('Product with ASIN %s could not be found.', asin)
                continue

            products[asin] = product

        if len(products) == 0:
            logger.error('For the given ASINs {} no products where found!'.format(','.join(asin_list)))
            return True

        logger.info('Synchronizing products with ItemIds %s', ', '.join(products.keys()))

        # query Amazon and iterate over results to update values
        for asin, amazon_data in ProductAdvertisingAPI().item_lookup(item_ids=list(products.keys())).items():
            self.__sync_product(products[asin], amazon_data)

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
        price = Price.objects.create(
            value=amazon_data['price'] if 'price' in amazon_data else None,
            currency=amazon_data['currency'] if 'currency' in amazon_data else None,
            date_seen=now,
            product=product,
        )

        product.current_price = price

        if product.lowest_price is None or (price.value is not None and price.value <= product.lowest_price.value):
            product.lowest_price = price

        if product.highest_price is None or (price.value is not None and price.value >= product.highest_price.value):
            product.highest_price = price

        # remove the elements that are not a field in Product model
        if 'price' in amazon_data:
            amazon_data.pop('price')
        if 'currency' in amazon_data:
            amazon_data.pop('currency')

        # update and save the product
        product.__dict__.update(amazon_data)
        product.status = 1
        product.date_last_synced = now
        product.save()

        if price.value is not None:
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
                NotifySubscriberTask().apply_async((product.pk, price.pk, sub.pk), countdown=5)


class NotifySubscriberTask(Task):
    """
    Task for notifying a single user about a product that has reached the desired price.
    """

    def run(self, product_pk, price_pk, subscription_pk, **kwargs):
        """
        Sends an email to the subscriber.
        :param product_pk: the id of product to notify about
        :type product_pk: int
        :param price_pk: the id of current price of the product
        :type price_pk: int
        :param subscription_pk: the id of Subscription class connecting subscriber and product
        :type subscription_pk: int
        """
        try:
            product = Product.objects.get(pk=product_pk)
        except Product.DoesNotExist:
            logger.error('Product with PK %d could not be found.', product_pk)
            return False

        try:
            price = Price.objects.get(pk=price_pk)
        except Price.DoesNotExist:
            logger.error('Price with PK %d could not be found.', price_pk)
            return False

        try:
            subscription = Subscription.objects.get(pk=subscription_pk)
        except Subscription.DoesNotExist:
            logger.error('Subscription with PK %d could not be found.', subscription_pk)
            return False

        logger.info('Trying to send notification email to %(email)s...' % {'email': subscription.email_notification.email})
        try:
            send_mail(product, subscription, price)
        except SMTPServerDisconnected:
            logger.exception('SMTP server was disconnected.')
        else:
            logger.info('Notification email to %(email)s was sent!' % {'email': subscription.email_notification.email})
            subscription.date_last_notification = timezone.now()
            subscription.save()
            return True

        return False
