from django import forms
from django.utils.translation import ugettext as _

from price_monitor.models import Product

class MultiASINForm(forms.Form):
    asins = forms.CharField(
        label=_('ASINs'),
        widget=forms.Textarea(
            attrs={'rows': 1}
        )
    )
