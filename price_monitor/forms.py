from . import app_settings as settings
from .models.EmailNotification import EmailNotification
from .models.Product import Product
from .models.Subscription import Subscription

from django import forms
from django.utils.translation import ugettext as _


class SubscriptionCreationForm(forms.ModelForm):
    """
    Form for creating an product Subscription
    """
    product = forms.RegexField(label=_('ASIN'), regex=settings.PRICE_MONITOR_ASIN_REGEX)
    email_notification = forms.ModelChoiceField(queryset=EmailNotification.objects.all(), empty_label=None)

    def clean_product(self):
        """
        At creation, user gives an ASIN. But for saving the model, a product
        instance is needed. So this product is looked up or created if not
        present here.
        """
        asin = self.cleaned_data['product']
        try:
            product = Product.objects.get(asin__iexact=asin)
        except Product.DoesNotExist:
            product = Product.objects.create(asin=asin)
        asin = product
        return asin

    class Meta:
        fields = ('product', 'email_notification', 'price_limit', 'owner')
        model = Subscription
        widgets = {
            'owner': forms.HiddenInput(),
        }


class SubscriptionUpdateForm(forms.ModelForm):
    class Meta:
        fields = ('product', 'email_notification', 'price_limit', 'owner')
        model = Subscription
        widgets = {
            'owner': forms.HiddenInput(),
            'product': forms.TextInput(attrs={'readonly': True}),
        }


class EmailNotificationForm(forms.ModelForm):
    class Meta:
        fields = ('email', 'owner')
        model = EmailNotification
        widgets = {
            'owner': forms.HiddenInput(),
        }
