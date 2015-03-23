from django.test import TestCase

from unittest.mock import patch

from price_monitor.product_advertising_api.api import ProductAdvertisingAPI

from testfixtures import log_capture


class ProductAdvertisingAPITest(TestCase):
    """
    Test class for the ProductAdvertisingAPI.
    """

    @patch('bottlenose.Amazon')
    @log_capture()
    def test_item_lookup_response_fail(self, amazon, log_capture):
        """
        Test for a product whose amazon query returns nothing
        """
        # mock the return value of amazon call
        amazon.ItemLookup.return_value = ''

        api = ProductAdvertisingAPI()
        api.item_lookup('XXX')

        # check log output
        log_capture.check(
            ('price_monitor.product_advertising_api', 'ERROR', 'Request for item lookup (ResponseGroup: Large, ASIN: XXX) was not valid')
        )

    def test_item_lookup_normal(self):
        """
        Test for a normal product.
        """
        # TODO implement

    def test_item_lookup_no_price(self):
        """
        Test for a product without price.
        """
        # TODO implement

    def test_item_lookup_no_audience_rating(self):
        """
        Test for a product without audience rating.
        """
        # TODO implement
