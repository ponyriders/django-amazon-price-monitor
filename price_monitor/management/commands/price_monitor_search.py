import traceback

from price_monitor.utils import get_api

from amazon.api import (
    AsinNotFound,
    LookupException,
)

from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.utils.translation import ugettext as _

from pprint import pprint


class Command(BaseCommand):
    """
    Command for batch creating of products.
    """
    args = '<ASIN>'
    help = 'Searches for a product with the given ASIN and prints out its details.'

    def handle(self, *args, **options):
        """
        Searches for a product with the given ASIN.
        """
        if len(args) != 1:
            raise CommandError(_('Please specify a single ASIN as only argument!'))

        try:
            product = get_api().lookup(ItemId=args[0])
        except (LookupException, AsinNotFound, UnicodeEncodeError):
            traceback.print_exc()
        else:
            pprint(
                {
                    'ASIN': product.asin,
                    'ISBN': product.isbn,
                    'EISBN': product.eisbn,
                    'EAN': product.ean,
                    'UPC': product.upc,
                    'SKU': product.sku,
                    'MPN': product.mpn,
                    'Parent ASIN': product.parent_asin,
                    'Title': product.title,
                    'Author': product.author,
                    'Authors': product.authors,
                    'Publisher': product.publisher,
                    'Label': product.label,
                    'Manufacturer': product.manufacturer,
                    'Brand': product.brand,
                    'Binding': product.binding,
                    'Pages': product.pages,
                    'Publication date': product.publication_date,
                    'Release date': product.release_date,
                    'Edition': product.edition,
                    'Offer-URL': product.offer_url,
                    'Large image URL': product.large_image_url,
                    'Medium image URL': product.medium_image_url,
                    'Small image URL': product.small_image_url,
                    'Tiny image URL': product.tiny_image_url,
                    'Reviews': product.reviews,
                    'Model': product.model,
                    'Part number': product.part_number,
                    'Editorial review': product.editorial_review,
                    'Features': product.features,
                    'Price & currency': product.price_and_currency,
                    'List price': product.list_price,

                },
                indent=4,
            )
