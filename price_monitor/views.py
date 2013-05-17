from django.views.generic.edit import CreateView

from price_monitor.forms import ProductForm
from price_monitor.models import Product

class ProductCreateView(CreateView):
    form_class = ProductForm
    model = Product
