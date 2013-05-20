from .. import app_settings as settings
from ..api import get_api
from amazon.api import AmazonProduct, LookupException
from celery.task import PeriodicTask
from datetime import timedelta
from price_monitor.models import Product


class ProductSynchronizeTask(PeriodicTask):
    """
    Synchronizes Products in status "Created" (0) initially with Product API.
    """
    run_every = timedelta(minutes=5)

    def run(self, **kwargs):
        #get all relevant products
        products = {p.asin: p for p in Product.objects.filter(status=0).order_by('date_creation')[:settings.PRODUCT_SYNCHRONIZE_COUNT]}

        # exit if there is no food
        if len(products) == 0:
            return

        try:
            lookup = get_api().lookup(ItemId=','.join(products.keys()))
        except LookupException:
            # TODO specify exceptions and handle appropriate
            import traceback
            traceback.print_exc()
            traceback.print_stack()
        except:
            # TODO specify exceptions and handle appropriate
            import traceback
            traceback.print_exc()
            traceback.print_stack()
        else:
            if type(lookup) == AmazonProduct:
                lookup = [lookup]

            for p in lookup:
                products[p.asin].title = p.title
                products[p.asin].large_image_url = p.large_image_url
                products[p.asin].medium_image_url = p.medium_image_url
                products[p.asin].small_image_url = p.small_image_url
                products[p.asin].tiny_image_url = p.tiny_image_url
                products[p.asin].offer_url = p.offer_url
                products[p.asin].status = 1
                products[p.asin].save()
