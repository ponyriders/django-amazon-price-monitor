"""Celery tasks for the Amazon Product Advertising API"""
import logging

from celery import chord
from celery.signals import celeryd_after_setup
from celery.task import (
    PeriodicTask,
    Task,
)
from celery.task.control import (
    inspect,
    revoke,
)

from collections import (
    Counter,
    namedtuple,
)

from datetime import (
    datetime,
    timedelta,
)

from django.db.models import (
    Min,
    Q,
)
from django.utils import timezone

# from django.utils.translation import ugettext

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

    """The task for getting the machinery up and running. As we do not use celery beat, we have to start somewhere."""

    ignore_result = True

    def run(self):
        logger.info('StartupTask was called')

        # that's better than an simple tuple
        task_repr = namedtuple('TaskRepresentation', 'id, name')

        # fetch all currently queued task, map them to the TaskRepresentation tuple
        scheduled_tasks = [task_repr(x['request']['id'], x['request']['name']) for x in list(inspect().scheduled().values())[0]]

        # count how many FindProductsToSynchronizeTask are scheduled
        count = dict(Counter([x.name for x in scheduled_tasks]).most_common())

        # check if the FindProductsToSynchronizeTask is in and how often
        if count:
            c = count[FindProductsToSynchronizeTask.name]
        else:
            c = 0

        # if the task is not scheduled, do so
        if c == 0:
            logger.info('no FindProductsToSynchronizeTask is scheduled, now scheduling it')
            FindProductsToSynchronizeTask().apply_async(countdown=5)

        # put out logging info if the task is already scheduled
        if c == 1:
            logger.info('FindProductsToSynchronizeTask is already scheduled, skipping additional run')

        # if the task is there more than once, remove it
        # this has the potential to remove ALL scheduled FindProductsToSynchronizeTasks if the timing is "bad"
        # however, the JumpStartTask will re-schedule the task if this happens (a workaround for a workaround - bad design by me btw.)
        if c > 1:
            logger.info('FindProductsToSynchronizeTask is already scheduled %d times, revoking %d', c, c - 1)

            # revoke c-1 tasks - that means the task still stays in schedule but is removed and not executed when execution time is reached
            for t in scheduled_tasks[1:]:
                logger.info('revoking FindProductsToSynchronizeTask with id %s', t.id)
                revoke(t.id)


class JumpStartTask(PeriodicTask):

    """
    Task providing jump start to the FindProductsToSynchronizeTask.

    It can happen that the FindProductsToSynchronizeTask does not reschedule itself. I don't know why. We do a workaround with this periodic tasks providing a
    jumper cable to reschedule the task by queuing the StartupTask.
    """

    run_every = timedelta(minutes=60)

    def run(self):
        """
        Does no more that to call the StartupTask in 5 seconds.

        :return: always True
        """
        logger.info('JumpStartTask was called')
        StartupTask().apply_async(countdown=5)
        return True


class FindProductsToSynchronizeTask(Task):

    """The tasks that finds the products that shall be updated through the api."""

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

        if products:
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

    """Task for synchronizing a single product."""

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

        if not products:
            logger.error('For the given ASINs %s no products where found!', ','.join(asin_list))
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

    """Task for notifying a single user about a product that has reached the desired price."""

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

        logger.info('Trying to send notification email to %s...', subscription.email_notification.email)
        try:
            send_mail(product, subscription, price, self.get_audience_rating_info(product))
        except SMTPServerDisconnected:
            logger.exception('SMTP server was disconnected.')
        else:
            logger.info('Notification email to %s was sent!', subscription.email_notification.email)
            subscription.date_last_notification = timezone.now()
            subscription.save()
            return True

        return False

    # TODO move to Product
    def get_audience_rating_info(self, product):
        """
        Checks, if the product matches specific audience rating and includes additional information.

        If the region is DE and the product is a FSK 18 one, additionally get all other FSK 18 products and put them into a mailable list.
        see https://github.com/ponyriders/django-amazon-price-monitor/issues/92

        As we do not currently have any use cases that could be generalized to something using the audience rating this is a country specific implementation.
        :param product: the product to check
        :type product:  price_monitor.models.Product
        :return: an additional mail text or empty string if product and installation do not match prerequisites.
        :rtype: str
        """
        # age_identifiers = ['Freigegeben ab 18 Jahren', 'Ages 18 and over']
        # if app_settings.PRICE_MONITOR_AMAZON_PRODUCT_API_REGION == 'DE' and product.audience_rating in age_identifiers:
        #     # mail text
        #     mail_text = ''
        #
        #     # fetch all other products with FSK 18
        #     for p in Product.objects.filter(audience_rating__in=age_identifiers).exclude(pk=product.pk).order_by('current_price'):
        #         mail_text += '{title:s}\n'.format(title=p.get_title())
        #         mail_text += '{price:0.2f} {currency:s} ({price_date:s})\n'.format(
        #             price=p.current_price.value,
        #             currency=p.current_price.currency,
        #             price_date=p.current_price.date_seen.strftime('%b %d, %Y %H:%M %p %Z'),
        #         )
        #         mail_text += '{offer_url:s}\n'.format(offer_url=p.offer_url)
        #         mail_text += '{product_detail_url:s}\n\n'.format(product_detail_url=product.get_detail_url())
        #
        #     # prepend introduction if there were results
        #     if mail_text:
        #         mail_text = '\n{intro:s}\n\n'.format(
        #             intro=ugettext('As this is a FSK 18 article, here are your other subscribed FSK 18 articles:')
        #         ) + mail_text
        #
        #     # return
        #     return mail_text
        return ''
