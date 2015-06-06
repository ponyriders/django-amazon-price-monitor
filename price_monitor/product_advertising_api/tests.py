import datetime

from bs4 import BeautifulSoup

from django.test import TestCase

from unittest.mock import patch

from price_monitor.product_advertising_api.api import ProductAdvertisingAPI
from price_monitor.product_advertising_api.test_data import (
    product_sample_10_products,
    product_sample_lookup_fail,
    product_sample_no_audience_rating,
    product_sample_no_item,
    product_sample_no_offers,
    product_sample_no_price,
    product_sample_ok,
)

from testfixtures import log_capture


class ProductAdvertisingAPITest(TestCase):
    """
    Test class for the ProductAdvertisingAPI.
    """

    def __get_product_bs(self, xml):
        """
        Wraps the given xml string into BeautifulSoup just as bottlenose does.
        :param xml: the xml to use
        :return: searchable bs object
        """
        return BeautifulSoup(xml)

    @patch.object(ProductAdvertisingAPI, 'lookup_at_amazon')
    @patch.object(ProductAdvertisingAPI, '__init__')
    @log_capture()
    def test_item_lookup_response_fail(self, papi_init, papi_lookup, lc):
        """
        Test for a product whose amazon query returns nothing.
        :param papi_init: mockup for ProductAdvertisingAPI.__init__
        :type papi_init: unittest.mock.MagicMock
        :param papi_lookup: mockup for ProductAdvertisingAPI.lookup_at_amazon
        :type papi_init: unittest.mock.MagicMock
        :param lc: log capture instance
        :type lc: testfixtures.logcapture.LogCaptureForDecorator
        """
        # mock the return value of amazon call
        papi_init.return_value = None
        papi_lookup.return_value = self.__get_product_bs('')

        api = ProductAdvertisingAPI()
        self.assertEqual(None, api.item_lookup(['ASIN-DUMMY']))

        # check log output
        lc.check(
            ('price_monitor.product_advertising_api', 'INFO', 'starting lookup for ASINs ASIN-DUMMY'),
            ('price_monitor.product_advertising_api', 'ERROR', 'Request for item lookup (ResponseGroup: Large, ASINs: ASIN-DUMMY) returned nothing')
        )

    @patch.object(ProductAdvertisingAPI, 'lookup_at_amazon')
    @patch.object(ProductAdvertisingAPI, '__init__')
    @log_capture()
    def test_item_lookup_fail(self, papi_init, papi_lookup, lc):
        """
        Test for a product which failed at the amazon endpoint.
        :param papi_init: mockup for ProductAdvertisingAPI.__init__
        :type papi_init: unittest.mock.MagicMock
        :param papi_lookup: mockup for ProductAdvertisingAPI.lookup_at_amazon
        :type papi_init: unittest.mock.MagicMock
        :param lc: log capture instance
        :type lc: testfixtures.logcapture.LogCaptureForDecorator
        """
        papi_init.return_value = None
        papi_lookup.return_value = self.__get_product_bs(product_sample_lookup_fail)

        api = ProductAdvertisingAPI()
        self.assertEqual(None, api.item_lookup(['DEMOASIN01']))

        # check log output
        lc.check(
            ('price_monitor.product_advertising_api', 'INFO', 'starting lookup for ASINs DEMOASIN01'),
            ('price_monitor.product_advertising_api', 'ERROR', 'Request for item lookup (ResponseGroup: Large, ASINs: DEMOASIN01) was not valid')
        )

    @patch.object(ProductAdvertisingAPI, 'lookup_at_amazon')
    @patch.object(ProductAdvertisingAPI, '__init__')
    @log_capture()
    def test_item_lookup_no_item(self, papi_init, papi_lookup, lc):
        """
        Test for a product with no returned items.
        :param papi_init: mockup for ProductAdvertisingAPI.__init__
        :type papi_init: unittest.mock.MagicMock
        :param papi_lookup: mockup for ProductAdvertisingAPI.lookup_at_amazon
        :type papi_init: unittest.mock.MagicMock
        :param lc: log capture instance
        :type lc: testfixtures.logcapture.LogCaptureForDecorator
        """
        papi_init.return_value = None
        papi_lookup.return_value = self.__get_product_bs(product_sample_no_item)

        api = ProductAdvertisingAPI()
        self.assertEqual(None, api.item_lookup(['DEMOASIN02']))

        # check log output
        lc.check(
            ('price_monitor.product_advertising_api', 'INFO', 'starting lookup for ASINs DEMOASIN02'),
            ('price_monitor.product_advertising_api', 'ERROR', 'Lookup for the following ASINs failed: DEMOASIN02')
        )

    @patch.object(ProductAdvertisingAPI, 'lookup_at_amazon')
    @patch.object(ProductAdvertisingAPI, '__init__')
    @log_capture()
    def test_item_lookup_normal(self, product_api_init, product_api_lookup, lc):
        """
        Test for a normal bluray.
        :param product_api_init: mockup for ProductAdvertisingAPI.__init__
        :type product_api_init: unittest.mock.MagicMock
        :param product_api_lookup: mockup for ProductAdvertisingAPI.lookup_at_amazon
        :type product_api_lookup: unittest.mock.MagicMock
        :param lc: log capture instance
        :type lc: testfixtures.logcapture.LogCaptureForDecorator
        """
        product_api_init.return_value = None
        product_api_lookup.return_value = self.__get_product_bs(product_sample_ok)

        api = ProductAdvertisingAPI()
        values = api.item_lookup(['DEMOASIN03'])

        # ensure the mocks were called
        self.assertTrue(product_api_init.called)
        self.assertTrue(product_api_lookup.called)

        self.assertNotEqual(None, values)
        self.assertEqual(type(dict()), type(values))
        self.assertEqual(len(values), 1)

        self.assertTrue('DEMOASIN03' in values)
        self.assertEqual('DEMOASIN03', values['DEMOASIN03']['asin'])
        self.assertEqual('Demo Series - Season 2 [Blu-ray]', values['DEMOASIN03']['title'])
        self.assertEqual(None, values['DEMOASIN03']['isbn'])
        self.assertEqual(None, values['DEMOASIN03']['eisbn'])
        self.assertEqual('Blu-ray', values['DEMOASIN03']['binding'])
        self.assertEqual(datetime.datetime(2014, 12, 22), values['DEMOASIN03']['date_publication'])
        self.assertEqual(datetime.datetime(2014, 12, 22), values['DEMOASIN03']['date_release'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN03IMAGE.jpg', values['DEMOASIN03']['large_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN03IMAGE._SL160_.jpg', values['DEMOASIN03']['medium_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN03IMAGE._SL75_.jpg', values['DEMOASIN03']['small_image_url'])
        self.assertEqual('http://www.amazon.de/dp/DEMOASIN03/?tag=sample-assoc-tag', values['DEMOASIN03']['offer_url'])
        self.assertEqual(16, values['DEMOASIN03']['audience_rating'])
        self.assertEqual(17.99, values['DEMOASIN03']['price'])
        self.assertEqual('EUR', values['DEMOASIN03']['currency'])

        # check log output
        lc.check(
            ('price_monitor.product_advertising_api', 'INFO', 'starting lookup for ASINs DEMOASIN03')
        )

    @patch.object(ProductAdvertisingAPI, 'lookup_at_amazon')
    @patch.object(ProductAdvertisingAPI, '__init__')
    @log_capture()
    def test_item_lookup_no_price(self, product_api_init, product_api_lookup, lc):
        """
        Test for a dvd without a price. Happens mostly for box sets.
        :param product_api_init: mockup for ProductAdvertisingAPI.__init__
        :type product_api_init: unittest.mock.MagicMock
        :param product_api_lookup: mockup for ProductAdvertisingAPI.lookup_at_amazon
        :type product_api_lookup: unittest.mock.MagicMock
        :param lc: log capture instance
        :type lc: testfixtures.logcapture.LogCaptureForDecorator
        """
        product_api_init.return_value = None
        product_api_lookup.return_value = self.__get_product_bs(product_sample_no_price)

        api = ProductAdvertisingAPI()
        values = api.item_lookup(['DEMOASIN04'])

        # ensure the mocks were called
        self.assertTrue(product_api_init.called)
        self.assertTrue(product_api_lookup.called)

        self.assertNotEqual(None, values)
        self.assertEqual(type(dict()), type(values))
        self.assertEqual(len(values), 1)

        self.assertTrue('DEMOASIN04' in values)
        self.assertEqual('DEMOASIN04', values['DEMOASIN04']['asin'])
        self.assertEqual('Another Demo Series - Season 1 (8 DVDs)', values['DEMOASIN04']['title'])
        self.assertEqual(None, values['DEMOASIN04']['isbn'])
        self.assertEqual(None, values['DEMOASIN04']['eisbn'])
        self.assertEqual('DVD', values['DEMOASIN04']['binding'])
        # dateutil.parser.parse will find out the year and month of "2004-11" but as there is no day, the day is set to the current day
        self.assertEqual(datetime.datetime(2004, 11, datetime.datetime.now().day), values['DEMOASIN04']['date_publication'])
        self.assertEqual(datetime.datetime(2004, 10, 27), values['DEMOASIN04']['date_release'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN04IMAGE.jpg', values['DEMOASIN04']['large_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN04IMAGE._SL160_.jpg', values['DEMOASIN04']['medium_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN04IMAGE._SL75_.jpg', values['DEMOASIN04']['small_image_url'])
        self.assertEqual('http://www.amazon.de/dp/DEMOASIN04/?tag=sample-assoc-tag', values['DEMOASIN04']['offer_url'])
        self.assertEqual(16, values['DEMOASIN04']['audience_rating'])

        # check log output
        lc.check(
            ('price_monitor.product_advertising_api', 'INFO', 'starting lookup for ASINs DEMOASIN04')
        )

    @patch.object(ProductAdvertisingAPI, 'lookup_at_amazon')
    @patch.object(ProductAdvertisingAPI, '__init__')
    @log_capture()
    def test_item_lookup_no_audience_rating_isbn(self, product_api_init, product_api_lookup, lc):
        """
        Test for a book without audience rating.
        :param product_api_init: mockup for ProductAdvertisingAPI.__init__
        :type product_api_init: unittest.mock.MagicMock
        :param product_api_lookup: mockup for ProductAdvertisingAPI.lookup_at_amazon
        :type product_api_lookup: unittest.mock.MagicMock
        :param lc: log capture instance
        :type lc: testfixtures.logcapture.LogCaptureForDecorator
        """
        product_api_init.return_value = None
        product_api_lookup.return_value = self.__get_product_bs(product_sample_no_audience_rating)

        api = ProductAdvertisingAPI()
        values = api.item_lookup(['123456789X'])

        # ensure the mocks were called
        # ensure the mocks were called
        self.assertTrue(product_api_init.called)
        self.assertTrue(product_api_lookup.called)

        self.assertNotEqual(None, values)
        self.assertEqual(type(dict()), type(values))
        self.assertEqual(len(values), 1)

        self.assertTrue('123456789X' in values)
        self.assertEqual('123456789X', values['123456789X']['asin'])
        self.assertEqual('A Sample Book', values['123456789X']['title'])
        self.assertEqual('123456789X', values['123456789X']['isbn'])
        self.assertEqual(None, values['123456789X']['eisbn'])
        self.assertEqual('Taschenbuch', values['123456789X']['binding'])
        self.assertEqual(datetime.datetime(2014, 8, 18), values['123456789X']['date_publication'])
        self.assertEqual(datetime.datetime(2014, 8, 18), values['123456789X']['date_release'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/123456789XIMAGE.jpg', values['123456789X']['large_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/123456789XIMAGE._SL160_.jpg', values['123456789X']['medium_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/123456789XIMAGE._SL75_.jpg', values['123456789X']['small_image_url'])
        self.assertEqual('http://www.amazon.de/dp/123456789X/?tag=sample-assoc-tag', values['123456789X']['offer_url'])
        self.assertEqual(10.0, values['123456789X']['price'])
        self.assertEqual('EUR', values['123456789X']['currency'])

        # check log output
        lc.check(
            ('price_monitor.product_advertising_api', 'INFO', 'starting lookup for ASINs 123456789X')
        )

    @patch.object(ProductAdvertisingAPI, 'lookup_at_amazon')
    @patch.object(ProductAdvertisingAPI, '__init__')
    @log_capture()
    def test_item_lookup_no_offers(self, product_api_init, product_api_lookup, lc):
        """
        Test for a book without offers.
        :param product_api_init: mockup for ProductAdvertisingAPI.__init__
        :type product_api_init: unittest.mock.MagicMock
        :param product_api_lookup: mockup for ProductAdvertisingAPI.lookup_at_amazon
        :type product_api_lookup: unittest.mock.MagicMock
        :param lc: log capture instance
        :type lc: testfixtures.logcapture.LogCaptureForDecorator
        """
        product_api_init.return_value = None
        product_api_lookup.return_value = self.__get_product_bs(product_sample_no_offers)

        api = ProductAdvertisingAPI()
        values = api.item_lookup(['DEMOASIN05'])

        # ensure the mocks were called
        self.assertTrue(product_api_init.called)
        self.assertTrue(product_api_lookup.called)

        self.assertNotEqual(None, values)
        self.assertEqual(type(dict()), type(values))
        self.assertEqual(len(values), 1)

        self.assertTrue('DEMOASIN05' in values)
        self.assertEqual('DEMOASIN05', values['DEMOASIN05']['asin'])
        self.assertEqual('Sønderzeichen', values['DEMOASIN05']['title'])
        self.assertEqual(None, values['DEMOASIN05']['isbn'])
        self.assertEqual(None, values['DEMOASIN05']['eisbn'])
        self.assertEqual('Kindle Edition', values['DEMOASIN05']['binding'])
        self.assertEqual(datetime.datetime(2009, 10, 14), values['DEMOASIN05']['date_publication'])
        self.assertEqual(datetime.datetime(2009, 10, 14), values['DEMOASIN05']['date_release'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN05IMAGE.jpg', values['DEMOASIN05']['large_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN05IMAGE._SL160_.jpg', values['DEMOASIN05']['medium_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN05IMAGE._SL75_.jpg', values['DEMOASIN05']['small_image_url'])
        self.assertEqual('http://www.amazon.de/dp/DEMOASIN05/?tag=sample-assoc-tag', values['DEMOASIN05']['offer_url'])
        self.assertRaises(KeyError, lambda: values['DEMOASIN05']['audience_rating'])

        # check log output
        lc.check(
            ('price_monitor.product_advertising_api', 'INFO', 'starting lookup for ASINs DEMOASIN05')
        )

    @patch.object(ProductAdvertisingAPI, 'lookup_at_amazon')
    @patch.object(ProductAdvertisingAPI, '__init__')
    @log_capture()
    def test_item_lookup_10_products(self, product_api_init, product_api_lookup, lc):
        """
        Tests for parsing 10 products.
        :param product_api_init: mockup for ProductAdvertisingAPI.__init__
        :type product_api_init: unittest.mock.MagicMock
        :param product_api_lookup: mockup for ProductAdvertisingAPI.lookup_at_amazon
        :type product_api_lookup: unittest.mock.MagicMock
        :param lc: log capture instance
        :type lc: testfixtures.logcapture.LogCaptureForDecorator
        """
        product_api_init.return_value = None
        product_api_lookup.return_value = self.__get_product_bs(product_sample_10_products)

        api = ProductAdvertisingAPI()
        values = api.item_lookup([
            'DEMOASIN06',
            'DEMOASIN07',
            'DEMOASIN08',
            'DEMOASIN09',
            'DEMOASIN10',
            'DEMOASIN11',
            'DEMOASIN12',
            'DEMOASIN13',
            'DEMOASIN14',
            'DEMOASIN15',
        ])

        # ensure the mocks were called
        self.assertTrue(product_api_init.called)
        self.assertTrue(product_api_lookup.called)

        self.assertNotEqual(None, values)
        self.assertEqual(type(dict()), type(values))
        self.assertEqual(len(values), 10)

        # ASIN DEMOASIN06
        self.assertTrue('DEMOASIN06' in values)
        self.assertEqual('DEMOASIN06', values['DEMOASIN06']['asin'])
        self.assertEqual('Hot Shots! - Teil 1 + Teil 2 [2 DVDs]', values['DEMOASIN06']['title'])
        self.assertEqual(None, values['DEMOASIN06']['isbn'])
        self.assertEqual(None, values['DEMOASIN06']['eisbn'])
        self.assertEqual('DVD', values['DEMOASIN06']['binding'])
        self.assertEqual(datetime.datetime(2012, 10, 5), values['DEMOASIN06']['date_publication'])
        self.assertEqual(datetime.datetime(2008, 11, 7), values['DEMOASIN06']['date_release'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN06.jpg', values['DEMOASIN06']['large_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN06._SL160_.jpg', values['DEMOASIN06']['medium_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN06._SL75_.jpg', values['DEMOASIN06']['small_image_url'])
        self.assertEqual('http://www.amazon.de/dp/DEMOASIN06/?tag=sample-assoc-tag', values['DEMOASIN06']['offer_url'])
        self.assertEqual(12, values['DEMOASIN06']['audience_rating'])

        # ASIN DEMOASIN07
        self.assertTrue('DEMOASIN07' in values)
        self.assertEqual('DEMOASIN07', values['DEMOASIN07']['asin'])
        self.assertEqual('Greatest Hits', values['DEMOASIN07']['title'])
        self.assertEqual(None, values['DEMOASIN07']['isbn'])
        self.assertEqual(None, values['DEMOASIN07']['eisbn'])
        self.assertEqual('Audio CD', values['DEMOASIN07']['binding'])
        self.assertEqual(None, values['DEMOASIN07']['date_publication'])
        self.assertEqual(datetime.datetime(2004, 6, 14), values['DEMOASIN07']['date_release'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN07.jpg', values['DEMOASIN07']['large_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN07._SL160_.jpg', values['DEMOASIN07']['medium_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN07._SL75_.jpg', values['DEMOASIN07']['small_image_url'])
        self.assertEqual('http://www.amazon.de/dp/DEMOASIN07/?tag=sample-assoc-tag', values['DEMOASIN07']['offer_url'])
        self.assertRaises(KeyError, lambda: values['DEMOASIN07']['audience_rating'])

        # ASIN DEMOASIN08
        self.assertTrue('DEMOASIN08' in values)
        self.assertEqual('DEMOASIN08', values['DEMOASIN08']['asin'])
        self.assertEqual('Tyrannosaurus Hives', values['DEMOASIN08']['title'])
        self.assertEqual(None, values['DEMOASIN08']['isbn'])
        self.assertEqual(None, values['DEMOASIN08']['eisbn'])
        self.assertEqual('Audio CD', values['DEMOASIN08']['binding'])
        self.assertEqual(datetime.datetime(2004, 7, 19), values['DEMOASIN08']['date_publication'])
        self.assertEqual(datetime.datetime(2004, 7, 19), values['DEMOASIN08']['date_release'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN08.jpg', values['DEMOASIN08']['large_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN08._SL160_.jpg', values['DEMOASIN08']['medium_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN08._SL75_.jpg', values['DEMOASIN08']['small_image_url'])
        self.assertEqual('http://www.amazon.de/dp/DEMOASIN08/?tag=sample-assoc-tag', values['DEMOASIN08']['offer_url'])
        self.assertRaises(KeyError, lambda: values['DEMOASIN08']['audience_rating'])

        # ASIN DEMOASIN09
        self.assertTrue('DEMOASIN09' in values)
        self.assertEqual('DEMOASIN09', values['DEMOASIN09']['asin'])
        self.assertEqual('Moonlight & Valentino', values['DEMOASIN09']['title'])
        self.assertEqual(None, values['DEMOASIN09']['isbn'])
        self.assertEqual(None, values['DEMOASIN09']['eisbn'])
        self.assertEqual('DVD', values['DEMOASIN09']['binding'])
        self.assertEqual(None, values['DEMOASIN09']['date_publication'])
        self.assertEqual(datetime.datetime(2004, 8, 1), values['DEMOASIN09']['date_release'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN09.jpg', values['DEMOASIN09']['large_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN09._SL160_.jpg', values['DEMOASIN09']['medium_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN09._SL75_.jpg', values['DEMOASIN09']['small_image_url'])
        self.assertEqual('http://www.amazon.de/dp/DEMOASIN09/?tag=sample-assoc-tag', values['DEMOASIN09']['offer_url'])
        self.assertEqual(6, values['DEMOASIN09']['audience_rating'])

        # ASIN DEMOASIN10
        self.assertTrue('DEMOASIN10' in values)
        self.assertEqual('DEMOASIN10', values['DEMOASIN10']['asin'])
        self.assertEqual('Jeepers Creepers 1 & 2 [Deluxe Edition] [4 DVDs]', values['DEMOASIN10']['title'])
        self.assertEqual(None, values['DEMOASIN10']['isbn'])
        self.assertEqual(None, values['DEMOASIN10']['eisbn'])
        self.assertEqual('DVD', values['DEMOASIN10']['binding'])
        self.assertEqual(None, values['DEMOASIN10']['date_publication'])
        self.assertEqual(datetime.datetime(2004, 9, 7), values['DEMOASIN10']['date_release'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN10.jpg', values['DEMOASIN10']['large_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN10._SL160_.jpg', values['DEMOASIN10']['medium_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN10._SL75_.jpg', values['DEMOASIN10']['small_image_url'])
        self.assertEqual('http://www.amazon.de/dp/DEMOASIN10/?tag=sample-assoc-tag', values['DEMOASIN10']['offer_url'])
        self.assertEqual(16, values['DEMOASIN10']['audience_rating'])

        # ASIN DEMOASIN11
        self.assertTrue('DEMOASIN11' in values)
        self.assertEqual('DEMOASIN11', values['DEMOASIN11']['asin'])
        self.assertEqual('Wintersun', values['DEMOASIN11']['title'])
        self.assertEqual(None, values['DEMOASIN11']['isbn'])
        self.assertEqual(None, values['DEMOASIN11']['eisbn'])
        self.assertEqual('Audio CD', values['DEMOASIN11']['binding'])
        self.assertEqual(datetime.datetime(2004, 10, 5), values['DEMOASIN11']['date_publication'])
        self.assertEqual(datetime.datetime(2004, 9, 13), values['DEMOASIN11']['date_release'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN11.jpg', values['DEMOASIN11']['large_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN11._SL160_.jpg', values['DEMOASIN11']['medium_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN11._SL75_.jpg', values['DEMOASIN11']['small_image_url'])
        self.assertEqual('http://www.amazon.de/dp/DEMOASIN11/?tag=sample-assoc-tag', values['DEMOASIN11']['offer_url'])
        self.assertRaises(KeyError, lambda: values['DEMOASIN11']['audience_rating'])

        # ASIN DEMOASIN12
        self.assertTrue('DEMOASIN12' in values)
        self.assertEqual('DEMOASIN12', values['DEMOASIN12']['asin'])
        self.assertEqual('Farscape - Season 1 (8 DVDs)', values['DEMOASIN12']['title'])
        self.assertEqual(None, values['DEMOASIN12']['isbn'])
        self.assertEqual(None, values['DEMOASIN12']['eisbn'])
        self.assertEqual('DVD', values['DEMOASIN12']['binding'])
        self.assertEqual(datetime.datetime(2004, 11, datetime.datetime.now().day), values['DEMOASIN12']['date_publication'])
        self.assertEqual(datetime.datetime(2004, 10, 27), values['DEMOASIN12']['date_release'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN12.jpg', values['DEMOASIN12']['large_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN12._SL160_.jpg', values['DEMOASIN12']['medium_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN12._SL75_.jpg', values['DEMOASIN12']['small_image_url'])
        self.assertEqual('http://www.amazon.de/dp/DEMOASIN12/?tag=sample-assoc-tag', values['DEMOASIN12']['offer_url'])
        self.assertEqual(16, values['DEMOASIN12']['audience_rating'])

        # ASIN DEMOASIN13
        self.assertTrue('DEMOASIN13' in values)
        self.assertEqual('DEMOASIN13', values['DEMOASIN13']['asin'])
        self.assertEqual('Hurricane Bar', values['DEMOASIN13']['title'])
        self.assertEqual(None, values['DEMOASIN13']['isbn'])
        self.assertEqual(None, values['DEMOASIN13']['eisbn'])
        self.assertEqual('Audio CD', values['DEMOASIN13']['binding'])
        self.assertEqual(None, values['DEMOASIN13']['date_publication'])
        self.assertEqual(datetime.datetime(2005, 1, 21), values['DEMOASIN13']['date_release'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN13.jpg', values['DEMOASIN13']['large_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN13._SL160_.jpg', values['DEMOASIN13']['medium_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN13._SL75_.jpg', values['DEMOASIN13']['small_image_url'])
        self.assertEqual('http://www.amazon.de/dp/DEMOASIN13/?tag=sample-assoc-tag', values['DEMOASIN13']['offer_url'])
        self.assertEqual(0, values['DEMOASIN13']['audience_rating'])

        # ASIN DEMOASIN14
        self.assertTrue('DEMOASIN14' in values)
        self.assertEqual('DEMOASIN14', values['DEMOASIN14']['asin'])
        self.assertEqual('Silent Alarm', values['DEMOASIN14']['title'])
        self.assertEqual(None, values['DEMOASIN14']['isbn'])
        self.assertEqual(None, values['DEMOASIN14']['eisbn'])
        self.assertEqual('Audio CD', values['DEMOASIN14']['binding'])
        self.assertEqual(None, values['DEMOASIN14']['date_publication'])
        self.assertEqual(datetime.datetime(2007, 1, 2), values['DEMOASIN14']['date_release'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN14.jpg', values['DEMOASIN14']['large_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN14._SL160_.jpg', values['DEMOASIN14']['medium_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN14._SL75_.jpg', values['DEMOASIN14']['small_image_url'])
        self.assertEqual('http://www.amazon.de/dp/DEMOASIN14/?tag=sample-assoc-tag', values['DEMOASIN14']['offer_url'])
        self.assertRaises(KeyError, lambda: values['DEMOASIN14']['audience_rating'])

        # ASIN DEMOASIN15
        self.assertTrue('DEMOASIN15' in values)
        self.assertEqual('DEMOASIN15', values['DEMOASIN15']['asin'])
        self.assertEqual('Greatest Hits', values['DEMOASIN15']['title'])
        self.assertEqual(None, values['DEMOASIN15']['isbn'])
        self.assertEqual(None, values['DEMOASIN15']['eisbn'])
        self.assertEqual('Audio CD', values['DEMOASIN15']['binding'])
        self.assertEqual(datetime.datetime(2005, datetime.datetime.now().month, datetime.datetime.now().day), values['DEMOASIN15']['date_publication'])
        self.assertEqual(datetime.datetime(2005, 2, 7), values['DEMOASIN15']['date_release'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN15.jpg', values['DEMOASIN15']['large_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN15._SL160_.jpg', values['DEMOASIN15']['medium_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN15._SL75_.jpg', values['DEMOASIN15']['small_image_url'])
        self.assertEqual('http://www.amazon.de/dp/DEMOASIN15/?tag=sample-assoc-tag', values['DEMOASIN15']['offer_url'])
        self.assertRaises(KeyError, lambda: values['DEMOASIN15']['audience_rating'])

        # check log output
        lc.check(
            (
                'price_monitor.product_advertising_api',
                'INFO',
                'starting lookup for ASINs DEMOASIN06, DEMOASIN07, DEMOASIN08, DEMOASIN09, DEMOASIN10, DEMOASIN11, DEMOASIN12, DEMOASIN13, DEMOASIN14, '
                'DEMOASIN15'
            )
        )

    def test_format_datetime(self):
        """
        Tests the datetime formatter.
        """
        api = ProductAdvertisingAPI()
        self.assertEqual(api.format_datetime('2014-10-11'), datetime.datetime(2014, 10, 11))
        self.assertEqual(api.format_datetime('2012-12'), datetime.datetime(2012, 12, datetime.datetime.now().day))
        # dateutil will use today as day value, but if today is the 31st that would not fit for february, there is no 31st february
        day = datetime.datetime.now().day if datetime.datetime.now().day <= 28 else 28
        self.assertEqual(api.format_datetime('2015-02'), datetime.datetime(2015, 2, day))
