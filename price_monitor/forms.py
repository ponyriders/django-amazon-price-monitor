import re

from . import app_settings as settings

from django import forms
from django.utils.translation import ugettext as _


class CustomSubscriptionForm(forms.Form):
    asin = forms.RegexField(label=_('ASIN'), regex=settings.PRICE_MONITOR_ASIN_REGEX)
    email = forms.EmailField(label=_('E-Mail for notifications'))
    price = forms.DecimalField(label=_('Price to notify'), max_digits=2)
