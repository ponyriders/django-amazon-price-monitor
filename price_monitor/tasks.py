import logging

from . import app_settings as settings
from .api import get_api
from amazon.api import (
    AmazonProduct,
    AsinNotFound,
    LookupException,
)
from celery.task import PeriodicTask
from django.utils import timezone
from datetime import timedelta
from price_monitor.models import (
    Price,
    Product
)


logger = logging.getLogger('price_monitor')


class ProductSynchronizeTask(PeriodicTask):
    """
    Synchronizes Products in status "Created" (0) initially with Product API.
    """
    run_every = timedelta(minutes=5)

    def run(self, **kwargs):
        """
        Runs the synchronization by fetching settings.AMAZON_PRODUCT_SYNCHRONIZE_COUNT number of products and requests their data from Amazon.
        """
        products = self.get_products_to_sync()

        # exit if there is no food
        if len(products) == 0:
            logger.info('No products to sync.')
            return
        else:
            logger.info('Syncing %(count)d products.' % {'count': len(products)})

        try:
            lookup = get_api().lookup(ItemId=','.join(products.keys()))
        except (LookupException, AsinNotFound):
            # if the lookup for all ASINs fails, do one by one to get the erroneous one(s)
            for asin, product in products.items():
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

    def get_products_to_sync(self):
        """
        Returns the products to synchronize.
        These are newly created products with status "0" or products that are older than settings.AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES.
        :return: dictionary with the Products
        :rtype: dict
        """
        # prefer already synced products over newly created
        products = {
            p.asin: p for p in Product.objects.select_related().filter(
                date_last_synced__lte=(timezone.now() - timedelta(minutes=settings.AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES))
            )
        }

        if len(products) < settings.AMAZON_PRODUCT_SYNCHRONIZE_COUNT:
            # there is still some space for products to sync, append newly created if available
            products = dict(
                products.items() + {
                    p.asin: p for p in Product.objects.select_related().filter(status=0)
                        .order_by('date_creation')[:(settings.AMAZON_PRODUCT_SYNCHRONIZE_COUNT - len(products))]
                }.items()
            )

        return products

    def sync_product(self, amazon_product, product):
        """
        Synchronizes the given price_monitor.model.Product with the Amazon lookup product.
        :param amazon_product: the Amazon product
        :type amazon_product: amazon.api.AmazonProduct
        :param product: the product to update
        :type product: price_monitor.models.Product
        """
        now = timezone.now()

        product.title = amazon_product.title
        product.large_image_url = amazon_product.large_image_url
        product.medium_image_url = amazon_product.medium_image_url
        product.small_image_url = amazon_product.small_image_url
        product.tiny_image_url = amazon_product.tiny_image_url
        product.offer_url = amazon_product.offer_url
        product.status = 1
        product.date_last_synced = now
        product.save()

        price = amazon_product.price_and_currency

        if not price[0] is None:
            Price.objects.create(
                value=price[0],
                currency=price[1],
                date_seen=now,
                product=product,
            )
