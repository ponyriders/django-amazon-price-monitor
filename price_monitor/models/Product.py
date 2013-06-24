from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy


class Product(models.Model):
    """
    Product to be monitored
    """
    STATUS_CHOICES = (
        (0, _('Created'),),
        (1, _('Synced over API'),),
        (2, _('Unsynchable'),),
    )

    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of creation'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('Date of last update'))
    date_last_synced = models.DateTimeField(blank=True, null=True, verbose_name=_('Date of last synchronization'))
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Subscription', verbose_name=_('Subscribers'))
    title = models.CharField(blank=True, null=True, max_length=255, verbose_name=_('Title'))
    asin = models.CharField(max_length=100, verbose_name=_('ASIN'))
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0, verbose_name=_('Status'))
    large_image_url = models.URLField(blank=True, null=True, verbose_name=_('URL to large product image'))
    medium_image_url = models.URLField(blank=True, null=True, verbose_name=_('URL to medium product image'))
    small_image_url = models.URLField(blank=True, null=True, verbose_name=_('URL to small product image'))
    tiny_image_url = models.URLField(blank=True, null=True, verbose_name=_('URL to tiny product image'))
    offer_url = models.URLField(blank=True, null=True, verbose_name=_('URL to the offer'))

    def set_failed_to_sync(self):
        """
        Marks the product as failed to sync. This happens if the Amazon API request for this product fails.
        """
        self.status = 2
        self.save()

    def __unicode__(self):
        """
        Returns the unicode representation of the Product.
        :return: the unicode representation
        :rtype: unicode
        """
        return u'%(name)s (ASIN: %(asin)s)' % {
            'name': self.title if self.title is not None and len(self.title) > 0 else _('Unsynced Product'),
            'asin': self.asin,
        }

    class Meta:
        app_label = 'price_monitor'
        verbose_name = ugettext_lazy('Product')
        verbose_name_plural = ugettext_lazy('Products')
        ordering = ('title', 'asin', )
