from django.core.management.base import BaseCommand, CommandError

from price_monitor.models import Product


class Command(BaseCommand):
    args = '<asin>'
    help = 'recreates a product with the given asin. if product already exists, it is deleted'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Please specify an asin')

        product, created = Product.objects.get_or_create(asin=args[0])
        if not created:
            product.delete()
            Product.objects.create(asin=args[0])
