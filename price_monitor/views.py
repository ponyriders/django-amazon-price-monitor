from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
)

from price_monitor.forms import SubscriptionCreationForm
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
            post = self.request.POST.copy()
            post.update({'owner': self.request.user.pk })
            creation_form = SubscriptionCreationForm(post)
        else:
            creation_form = SubscriptionCreationForm()
        context['creation_form'] = creation_form
        return context

    def post(self, request, *args, **kwargs):
        parent_view = super(ProductListAndCreateView, self).get(request, *args, **kwargs)
        creation_form = parent_view.context_data['creation_form']
        if creation_form.is_valid():
            creation_form.save()
            return redirect('monitor_view')
        return parent_view

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """
        Overwritting this method the make every instance of the view
        login_required
        """
        return super(ProductListAndCreateView, self).dispatch(*args, **kwargs)
