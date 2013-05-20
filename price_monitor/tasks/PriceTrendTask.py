import logging

from .. import app_settings as settings
from ..api import get_api
from amazon.api import AmazonProduct, AsinNotFound, LookupException
from celery.task import PeriodicTask
from datetime import timedelta
from price_monitor.models import Product


logger = logging.getLogger('price_monitor')


class PriceTrendTask(PeriodicTask):
    """
    Fetches the prices for all available products.
    """
    run_every = timedelta(hours=6)

    def run(self, **kwargs):
        pass
