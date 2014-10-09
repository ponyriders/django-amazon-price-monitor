from django.conf import settings
from django.db import models
from django.utils import formats
from django.utils.translation import ugettext as _, ugettext_lazy

from price_monitor import app_settings

# FIXME do not use six, distinguish python versions directly
from six import text_type
from six.moves.urllib.parse import (
    urljoin,
    urlparse,
)


class Product(models.Model):
    """
    Product to be monitored
    """
    STATUS_CHOICES = (
        (0, _('Created'),),
        (1, _('Synced over API'),),
        (2, _('Unsynchable'),),
    )

    # date values
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of creation'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('Date of last update'))
    date_last_synced = models.DateTimeField(blank=True, null=True, verbose_name=_('Date of last synchronization'))

    # synchronization status
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0, verbose_name=_('Status'))

    # relations
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Subscription', verbose_name=_('Subscribers'))

    # amazon specific fields
    asin = models.CharField(max_length=100, unique=True, verbose_name=_('ASIN'))
    title = models.CharField(blank=True, null=True, max_length=255, verbose_name=_('Title'))
    isbn = models.CharField(blank=True, null=True, max_length=10, verbose_name=_('ISBN'))
    eisbn = models.CharField(blank=True, null=True, max_length=13, verbose_name=_('E-ISBN'))
    binding = models.CharField(blank=True, null=True, max_length=255, verbose_name=_('Binding'))
    date_publication = models.DateField(blank=True, null=True, verbose_name=_('Publication date'))
    date_release = models.DateField(blank=True, null=True, verbose_name=_('Release date'))
    audience_rating = models.CharField(blank=True, null=True, max_length=255, verbose_name=_('Audience rating'))
    large_image_url = models.URLField(blank=True, null=True, verbose_name=_('URL to large product image'))
    medium_image_url = models.URLField(blank=True, null=True, verbose_name=_('URL to medium product image'))
    small_image_url = models.URLField(blank=True, null=True, verbose_name=_('URL to small product image'))
    tiny_image_url = models.URLField(blank=True, null=True, verbose_name=_('URL to tiny product image'))
    offer_url = models.URLField(blank=True, null=True, verbose_name=_('URL to the offer'))

    def get_prices_for_chart(self):
        """
        Returns all prices of the product.
        :return: list
        """
        # TODO: be able to specify a range, like last 100 days
        # TODO: don't select all prices, but a representative representation, like each 5th price aso
        return [{'x': str(formats.date_format(p.date_seen, 'SHORT_DATETIME_FORMAT')), 'y': p.value} for p in self.price_set.all().order_by('date_seen')]

    def set_failed_to_sync(self):
        """
        Marks the product as failed to sync. This happens if the Amazon API request for this product fails.
        """
        self.status = 2
        self.save()

    @staticmethod
    def __get_image_url(url):
        """
        Returns the correct image url depending on the settings. Will either be a HTTP or HTTPS host.
        :param url: the original (HTTP) image url
        :return: the adjusted image url if SSL is enabled
        """
        if url is None or not app_settings.PRICE_MONITOR_IMAGES_USE_SSL:
            return url
        else:
            return urljoin(app_settings.PRICE_MONITOR_AMAZON_SSL_IMAGE_DOMAIN, urlparse(url).path)

    def get_graph_cache_key(self):
        """
        Returns cache key used for caching the price graph
        :return: the cache key
        :rtype:  str
        """
        return 'graph-%s-%s' % (self.asin, self.date_last_synced.isoformat() if self.date_last_synced is not None else '')

    def __unicode__(self):
        """
        Returns the unicode representation of the Product.
        :return: the unicode representation
        :rtype: unicode
        """
        return text_type(
            '%(name)s (ASIN: %(asin)s)' % {
                'name': self.title if self.title is not None and len(self.title) > 0 else _('Unsynchronized Product'),
                'asin': self.asin,
            }
        )

    class Meta:
        app_label = 'price_monitor'
        verbose_name = ugettext_lazy('Product')
        verbose_name_plural = ugettext_lazy('Products')
        ordering = ('title', 'asin', )
