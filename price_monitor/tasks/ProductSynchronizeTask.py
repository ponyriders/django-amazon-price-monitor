import logging

from .. import app_settings as settings
from ..api import get_api
from amazon.api import AmazonProduct, AsinNotFound, LookupException
from celery.task import PeriodicTask
from datetime import timedelta
from price_monitor.models import Product


logger = logging.getLogger('price_monitor')


class ProductSynchronizeTask(PeriodicTask):
    """
    Synchronizes Products in status "Created" (0) initially with Product API.
    """
    run_every = timedelta(minutes=5)

    def run(self, **kwargs):
        """
        Runs the synchronization by fetching settings.PRODUCT_SYNCHRONIZE_COUNT number of products and requests their data from Amazon.
        """

        # get all relevant products
        products = {
            p.asin: p for p in Product.objects.filter(status=0).order_by('date_creation')[:settings.PRODUCT_SYNCHRONIZE_COUNT]
        }

        # exit if there is no food
        if len(products) == 0:
            logger.info('No products to sync.')
            return

        try:
            lookup = get_api().lookup(ItemId=','.join(products.keys()))
        except (LookupException, AsinNotFound):
            # if the lookup for all ASINs fails, do one by one to get the erroneous one(s)
            for asin, product in products.items():
                try:
                    lookup = get_api().lookup(ItemId=asin)
                except (LookupException, AsinNotFound):
                    logger.exception()
                    product.set_failed_to_sync()
                else:
                    self.sync_product(lookup, product)
        else:
            # api.lookup hides a list of AmazonProducts or a single AmazonProduct
            if type(lookup) == AmazonProduct:
                lookup = [lookup]

            # iterate an sync
            for p in lookup:
                self.sync_product(lookup, p)

    def sync_product(self, amazon_product, product):
        """
        Synchronizes the given price_monitor.model.Product with the Amazon lookup product.
        :param amazon_product: the Amazon product
        :type amazon_product: amazon.api.AmazonProduct
        :param product: the product to update
        :type product: price_monitor.models.Product
        """
        product.title = amazon_product.title
        product.large_image_url = amazon_product.large_image_url
        product.medium_image_url = amazon_product.medium_image_url
        product.small_image_url = amazon_product.small_image_url
        product.tiny_image_url = amazon_product.tiny_image_url
        product.offer_url = amazon_product.offer_url
        product.status = 1
        product.save()
