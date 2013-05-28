from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy


class Subscription(models.Model):
    """
    Model for a user being able to subscribe to a product and be notified if the price_limit is reached.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Owner'))
    product = models.ForeignKey('Product', verbose_name=_('Product'))
    price_limit = models.FloatField(verbose_name=_('Price limit'))

    class Meta:
        app_label = 'price_monitor'
        verbose_name = ugettext_lazy('Subscription')
        verbose_name_plural = ugettext_lazy('Subscriptions')
