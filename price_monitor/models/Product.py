from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy


class Product(models.Model):
    """
    Product wraps multiple SubProducts, because the same product can be available
    This is done because the same product, a DVD for example, can appear with multiple ASINs
    in Amazons database
    """
    users = models.ManyToManyField(User, verbose_name=ugettext_lazy('Users monitoring this product'))
    subproducts = models.ManyToManyField('SubProduct', verbose_name=ugettext_lazy('Subproducts'))

    class Meta:
        app_label = 'price_monitor'
        verbose_name = ugettext_lazy('Product')
        verbose_name_plural = ugettext_lazy('Products')
