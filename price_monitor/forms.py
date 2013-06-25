import re

from . import app_settings as settings
from .models.Product import Product
from .models.Subscription import Subscription

from django import forms
from django.utils.translation import ugettext as _


class SubscriptionCreationForm(forms.ModelForm):
    product = forms.RegexField(label=_('ASIN'), regex=settings.PRICE_MONITOR_ASIN_REGEX)

    class Meta:
        fields = ('product', 'email_notification', 'price_limit')
        model = Subscription

    def clean(self):
        cleaned_data = super(SubscriptionCreationForm, self).clean()
        try:
            product = Product.objects.get(asin=cleaned_data['product'])
        except Product.DoesNotExist:
            product = Product.objects.create(asin=cleaned_data['product'])
        cleaned_data['product'] = product
        return cleaned_data

class SubscriptionUpdateForm(forms.ModelForm):
    class Meta:
        fields = ('product', 'email_notification', 'price_limit')
        model = Subscription
        widgets = {
            'product': forms.TextInput(attrs={'readonly': True}),
        }
