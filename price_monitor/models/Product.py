from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy


class Product(models.Model):
    """
    Product to be monitored
    """
    users = models.ManyToManyField(User, verbose_name=ugettext_lazy('Users monitoring this product'))
    prices = models.ManyToManyField('Price', verbose_name=ugettext_lazy('Prices of Product'))

    class Meta:
        app_label = 'price_monitor'
        verbose_name = ugettext_lazy('Product')
        verbose_name_plural = ugettext_lazy('Products')
