from django.core.management.base import BaseCommand

from price_monitor.models import Product


class Command(BaseCommand):
    """
    Command for batch creating of products.
    """
    help = 'Creates multiple products from the given ASIN list. Skips products already in database.'

    def add_arguments(self, parser):
        """
        Adds the positional argument for ASINs
        """
        parser.add_argument('asins', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        Batch create products from given ASIN list.
        """
        # get all products with given asins
        product_asins = [p.asin for p in Product.objects.filter(asin__in=options['asins'])]

        # remove the asins that are already there
        asins = [a for a in options['asins'] if a not in product_asins]

        # create some products
        for asin in asins:
            Product.objects.create(asin=asin)

        print('created %d products' % len(asins))
