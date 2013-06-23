from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy


class Price(models.Model):
    value = models.FloatField(verbose_name=_('Price'))
    currency = models.CharField(max_length=3, verbose_name=_('Currency'))
    date_seen = models.DateTimeField(verbose_name=_('Date of price'))
    product = models.ForeignKey('Product', verbose_name=_('Product'))

    def __unicode__(self):
        """
        Returns the unicode representation of the Product.
        :return: the unicode representation
        :rtype: unicode
        """
        return u'%(value)0.2f %(currency)s on %(date_seen)s' % {
            'value': self.value,
            'currency': self.currency,
            'date_seen': self.date_seen,
        }

    class Meta:
        app_label = 'price_monitor'
        verbose_name = ugettext_lazy('Price')
        verbose_name_plural = ugettext_lazy('Prices')
