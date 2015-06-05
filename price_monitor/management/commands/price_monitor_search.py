from django.core.management.base import BaseCommand

from price_monitor.product_advertising_api.api import ProductAdvertisingAPI

from pprint import pprint


class Command(BaseCommand):
    """
    Command for batch creating of products.
    """
    help = 'Searches for a product at Amazon (not the DB!) with the given ASIN and prints out its details.'

    def add_arguments(self, parser):
        """
        Adds the positional argument for ASIN
        """
        parser.add_argument('asin', nargs=1, type=str)

    def handle(self, *args, **options):
        """
        Searches for a product with the given ASIN.
        """
        asin = options['asin'][0]
        api = ProductAdvertisingAPI()
        pprint(api.item_lookup(asin), indent=4)
