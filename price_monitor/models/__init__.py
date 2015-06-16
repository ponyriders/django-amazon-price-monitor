import os

from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver

from price_monitor.models.EmailNotification import EmailNotification  # noqa
from price_monitor.models.Price import Price  # noqa
from price_monitor.models.Product import Product  # noqa
from price_monitor.models.Subscription import Subscription  # noqa


@receiver(post_save, sender=Product)
def synchronize_product_after_creation(sender, instance, created, **kwargs):
    """
    Directly start synchronization of a Product after its creation.
    :param sender: class calling the signal
    :type sender: ModelBase
    :param instance: the Product instance
    :type instance: Product
    :param created: if the Product was created
    :type created: bool
    :param kwargs: additional keywords arguments, see https://docs.djangoproject.com/en/dev/ref/signals/#django.db.models.signals.post_save
    :type kwargs: dict
    """
    if created and os.environ.get('STAGE', 'Live') != 'TravisCI':
        from price_monitor.product_advertising_api.tasks import SynchronizeSingleProductTask
        SynchronizeSingleProductTask.delay([instance.asin])


@receiver(post_delete, sender=Subscription)
def cleanup_products_after_subscription_removal(sender, instance, using, **kwargs):
    """
    Queues the execution of the ProductCleanupTask after a subscription was deleted.
    :param sender: class calling the signal
    :type sender: ModelBase
    :param instance: the Subscription instance
    :type instance: price_monitor.models.Subscription
    :param using: database alias being used
    :type using: str
    :param kwargs: additional keywords arguments, see https://docs.djangoproject.com/en/dev/ref/signals/#django.db.models.signals.post_delete
    :type kwargs: dict
    """
    if os.environ.get('STAGE', 'Live') != 'TravisCI':
        from price_monitor.tasks import ProductCleanupTask
        ProductCleanupTask.delay(instance.product.asin)
