import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from . import app_settings
from .forms import SubscriptionCreationForm

logger = logging.getLogger('price_monitor')


class AngularIndexView(TemplateView):
    template_name = 'price_monitor/angular_index_view.html'
    form = SubscriptionCreationForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """
        Overwriting this method the make every instance of the view
        login_required
        :param args: positional arguments
        :type args: List
        :param kwargs: keyword arguments
        :type kwargs: Dict
        :return: Result of super method. As this dispatches the handling method
        for the incoming request and calls it, the return is a HttpResponse
        object
        :rtype: HttpResponse
        """
        return super(AngularIndexView, self).dispatch(*args, **kwargs)

    def get_context_data(self, form=None, **kwargs):
        context = super(AngularIndexView, self).get_context_data(**kwargs)
        context.update(
            default_currency=app_settings.PRICE_MONITOR_DEFAULT_CURRENCY,
            subscription_create_form=form,
            site_name=app_settings.PRICE_MONITOR_SITENAME,
            product_advertising_disclaimer=app_settings.PRICE_MONITOR_AMAZON_PRODUCT_ADVERTISING_API_DISCLAIMER,
            associate_disclaimer=app_settings.PRICE_MONITOR_ASSOCIATE_DISCLAIMER,
        )
        return context

    def get(self, request, **kwargs):
        form = self.form()
        context = self.get_context_data(form=form, **kwargs)
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        in_data = json.loads(request.body)
        form = self.form(data=in_data)
        response_data = {'errors': form.errors}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
