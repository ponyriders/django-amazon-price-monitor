from django import forms

from price_monitor.models import Product

class ProductForm(forms.ModelForm):
    fields = ['asin']

    class Meta:
        model = Product
