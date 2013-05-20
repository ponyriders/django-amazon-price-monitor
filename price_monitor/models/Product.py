from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy


class Product(models.Model):
    """
    Product to be monitored
    """
    STATUS_CHOICES = (
        (0, _('Created'),),
        (1, _('Synced over API'),),
    )

    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of creation'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('Date of last update'))
    users = models.ManyToManyField(User, blank=True, null=True, verbose_name=_('Users monitoring this product'))
    prices = models.ManyToManyField('Price', blank=True, null=True, verbose_name=_('Prices of Product'))
    title = models.CharField(blank=True, null=True, max_length=255, verbose_name=_('Title'))
    asin = models.CharField(max_length=100, verbose_name=_('ASIN'))
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0, verbose_name=_('Status'))
    large_image_url = models.URLField(blank=True, null=True, verbose_name=_('URL to large product image'))
    offer_url = models.URLField(blank=True, null=True, verbose_name=_('URL to the offer'))

    def __unicode__(self):
        """
        Returns the unicode representation of the Product.
        :return: the unicode representation
        :rtype: unicode
        """
        return u'%(name)s (ASIN: %(asin)s)' % {
            'name': self.title if len(self.title) > 0 else _('Unsynced Product'),
            'asin': self.asin,
        }

    class Meta:
        app_label = 'price_monitor'
        verbose_name = ugettext_lazy('Product')
        verbose_name_plural = ugettext_lazy('Products')
