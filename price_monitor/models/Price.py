from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy


class Price(models.Model):
    """
    Representing fetched price for a product
    """
    value = models.FloatField(verbose_name=_('Price'), blank=True, null=True)
    currency = models.CharField(max_length=3, verbose_name=_('Currency'), blank=True, null=True)
    date_seen = models.DateTimeField(verbose_name=_('Date of price'))
    product = models.ForeignKey('Product', verbose_name=_('Product'))

    def __str__(self):
        """
        Returns the string representation of the Product.
        :return: the unicode representation
        :rtype: unicode
        """
        return '%(value)s %(currency)s on %(date_seen)s' % dict(
            value='%0.2f' % self.value if self.value else 'No price',
            currency=self.currency if self.currency else '',
            date_seen=self.date_seen
        )

    class Meta:
        app_label = 'price_monitor'
        get_latest_by = 'date_seen'
        verbose_name = ugettext_lazy('Price')
        verbose_name_plural = ugettext_lazy('Prices')
        ordering = ('date_seen',)
