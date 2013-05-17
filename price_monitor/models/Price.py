from django.db import models
from django.utils.translation import ugettext_lazy


class Price(models.Model):
    value = models.FloatField(verbose_name=ugettext_lazy('Price'))
    date_seen = models.DateTimeField(verbose_name=ugettext_lazy('Date of price'))

    class Meta:
        app_label = 'price_monitor'
        verbose_name = ugettext_lazy('Price')
        verbose_name_plural = ugettext_lazy('Prices')
