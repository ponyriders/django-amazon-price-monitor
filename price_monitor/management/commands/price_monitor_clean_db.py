from django.core.management.base import BaseCommand

from price_monitor.models import (
    Price,
    Product,
)


class Command(BaseCommand):
    """
    Command for cleaning the database. Deletes all products without subscriptions.
    """
    help = 'Deletes all products without subscriptions'

    def handle(self, *args, **options):
        """
        Deletes the products without subscriptions.
        """
        products_without_subscribers = Product.objects.filter(subscribers__isnull=True)
        prices_without_subscribers = Price.objects.filter(product__subscribers__isnull=True)

        print('=== PRE-CLEANUP ==================================')
        print('Product count:                {:20d}'.format(Product.objects.count()))
        print('Products with subscribers:    {:20d}'.format(Product.objects.filter(subscribers__isnull=False).count()))
        print('Products without subscribers: {:20d}'.format(products_without_subscribers.count()))
        print('Prices count:                 {:20d}'.format(Price.objects.count()))
        print('==================================================')
        print('')

        choice = input(
            '{:d} products with {:d} prices will be deleted, continue? [y/N]'.format(
                products_without_subscribers.count(),
                prices_without_subscribers.count()
            )
        )

        if choice in ['y', 'Y']:
            products_without_subscribers.delete()
            prices_without_subscribers.delete()
            print('')
            print('DONE')
