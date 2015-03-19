from django.core.management.base import BaseCommand, CommandError

from price_monitor.models import Product


class Command(BaseCommand):
    args = '<asin>'
    help = 'adds a product with the given asin'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Please specify an asin')

        Product.objects.create(asin=args[0])
