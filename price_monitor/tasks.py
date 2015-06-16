import logging

from celery.task import Task

from price_monitor.models import (
    Price,
    Product,
    Subscription,
)


logger = logging.getLogger('price_monitor.tasks')


class ProductCleanupTask(Task):
    """
    Task for removing a product if it has no subscribers.
    """

    def run(self, asin):
        """
        Checks if there are subscribers for the product with the given asin. If not, the product and its prices are deleted.
        :param asin: the ASIN of the product
        :type asin: str
        :return: success or failure
        """
        try:
            product = Product.objects.get(asin=asin)
        except Product.DoesNotExist:
            logger.error('Product with ASIN %d does not exist, skipping ProductCleanupTask', asin)
            return

        subscribers = Subscription.objects.filter(product=product).count()

        if subscribers == 0:
            prices = Price.objects.filter(product=product)
            logger.info('Removing product with ASIN %s (PK: %d) and its %d prices', asin, product.pk, prices.count())
            prices.delete()
            product.delete()
            return True
