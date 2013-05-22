from django.views.generic import (
    CreateView,
    ListView,
)

from price_monitor.forms import ProductForm
from price_monitor.models import Product

class ProductListAndCreateView(CreateView, ListView):
    form_class = ProductForm
    model = Product

    template_name = 'price_monitor/list_and_create.html'
