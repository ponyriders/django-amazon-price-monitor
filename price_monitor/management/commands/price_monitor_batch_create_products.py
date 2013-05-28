from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _

from ...models import Product


class Command(BaseCommand):
    """
    Command for batch creating of products.
    """
    args = 'list of ASINs separated by comma'
    help = 'Creates multiple products from the given ASIN list. Skips products already in database.'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError(_('Please specify a list of ASINs as only argument, separated by comma!'))

        # make a list
        asins = args[0].split(',')

        # get all products with given asins
        product_asins = [p.asin for p in Product.objects.filter(asin__in=asins)]

        # remove the asins that are already there
        asins = filter(lambda a: a not in product_asins, asins)

        # create some products
        for asin in asins:
            Product.objects.create(asin=asin)

        print 'created %d products' % len(asins)
