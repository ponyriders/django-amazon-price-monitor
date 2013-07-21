from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
)

from .forms import SubscriptionCreationForm
from .formsets import SubscriptionModelFormset
from .models import (
    Product,
    Subscription,
)


class ProductListAndCreateView(ListView):
    model = Product

    template_name = 'price_monitor/product_list_and_create.html'
    template_name_suffix = ''

    def get_queryset(self):
        qs = super(ProductListAndCreateView, self).get_queryset()
        return qs.filter(subscription__owner=self.request.user.pk)

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListAndCreateView, self).get_context_data(*args, **kwargs)
        creation_formset_class = modelformset_factory(model=Subscription, formset=SubscriptionModelFormset, form=SubscriptionCreationForm)
        if self.request.method == 'POST':
            post = self.request.POST.copy()
            for i in range(int(self.request.POST.get('form-TOTAL_FORMS', 1000))):
                post.update({'form-%s-owner' % i: self.request.user.id})
            creation_formset = creation_formset_class(post, user=self.request.user)
        else:
            creation_formset = creation_formset_class(user=self.request.user, queryset=Subscription.objects.none())
        context['creation_formset'] = creation_formset
        return context

    def post(self, request, *args, **kwargs):
        parent_view = super(ProductListAndCreateView, self).get(request, *args, **kwargs)
        creation_formset = parent_view.context_data['creation_formset']
        if creation_formset.is_valid():
            creation_formset.save()
            return redirect('monitor_view')
        return parent_view

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """
        Overwritting this method the make every instance of the view
        login_required
        """
        return super(ProductListAndCreateView, self).dispatch(*args, **kwargs)
