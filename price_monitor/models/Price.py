from django.db import models
from django.utils.translation import ugettext_lazy

class Price(models.Model):
    value = models.FloatField(verbose_name=ugettext_lazy('Price'))
    date_seen = models.DateTimeField(verbose_name=ugettext_lazy('Date of price'))
