from django.test import TestCase

from price_monitor.product_advertising_api.api import ProductAdvertisingAPI


class ProductAdvertisingAPITest(TestCase):
    """
    Test class for the ProductAdvertisingAPI.
    """

    def setUp(self):
        self.api = ProductAdvertisingAPI()

    def tearDown(self):
        pass

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
