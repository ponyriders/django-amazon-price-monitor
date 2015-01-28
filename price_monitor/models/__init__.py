import os

from django.db.models.signals import post_save
from django.dispatch import receiver

from price_monitor.models.EmailNotification import EmailNotification
from price_monitor.models.Price import Price
from price_monitor.models.Product import Product
from price_monitor.models.Subscription import Subscription


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
    :param kwargs: additional keywords arguments, see https://docs.djangoproject.com/en/1.6/ref/signals/#django.db.models.signals.post_save
    :type kwargs: dict
    """
    if created and os.environ.get('STAGE', 'Live') != 'TravisCI':
        from price_monitor.product_advertising_api.tasks import SynchronizeSingleProductTask
        SynchronizeSingleProductTask.delay(instance.asin)
