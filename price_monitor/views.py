from django.views.generic import (
    ListView,
)

from price_monitor.forms import MultiASINForm
from price_monitor.models import Product

class ProductListAndCreateView(ListView):
    model = Product

    template_name = 'price_monitor/list_and_create.html'
    template_name_suffix = ''

    def get_queryset(self):
        qs = super(ProductListAndCreateView, self).get_queryset()
        return qs.filter(subscription__owner=self.request.user.pk)

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListAndCreateView, self).get_context_data(*args, **kwargs)
        if self.request.method == 'POST':
            form = MultiASINForm(self.request.POST)
        else:
            form = MultiASINForm()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        return super(ProductListAndCreateView, self).get(request, *args, **kwargs)
