import datetime

from bs4 import BeautifulSoup

from django.test import TestCase

from unittest.mock import patch

from price_monitor.product_advertising_api.api import ProductAdvertisingAPI

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
        self.assertEqual(None, api.item_lookup('ASIN-DUMMY'))

        # check log output
        lc.check(
            ('price_monitor.product_advertising_api', 'ERROR', 'Request for item lookup (ResponseGroup: Large, ASIN: ASIN-DUMMY) returned nothing')
        )

    product_sample_lookup_fail = """
        <?xml version="1.0" ?>
        <itemlookupresponse xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
            <items>
                <request>
                    <isvalid>False</isvalid>
                    <itemlookuprequest>
                        <idtype>ASIN</idtype>
                        <itemid>DEMOASIN01</itemid>
                        <responsegroup>Large</responsegroup>
                        <variationpage>All</variationpage>
                    </itemlookuprequest>
                </request>
            </items>
        </itemlookupresponse>
    """

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
        papi_lookup.return_value = self.__get_product_bs(self.product_sample_lookup_fail)

        api = ProductAdvertisingAPI()
        self.assertEqual(None, api.item_lookup('DEMOASIN01'))

        # check log output
        lc.check(
            ('price_monitor.product_advertising_api', 'ERROR', 'Request for item lookup (ResponseGroup: Large, ASIN: DEMOASIN01) was not valid')
        )

    product_sample_no_item = """
        <?xml version="1.0" ?>
        <itemlookupresponse xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
            <items>
                <request>
                    <isvalid>True</isvalid>
                    <itemlookuprequest>
                        <idtype>ASIN</idtype>
                        <itemid>DEMOASIN02</itemid>
                        <responsegroup>Large</responsegroup>
                        <variationpage>All</variationpage>
                    </itemlookuprequest>
                </request>
            </items>
        </itemlookupresponse>
    """

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
        papi_lookup.return_value = self.__get_product_bs(self.product_sample_no_item)

        api = ProductAdvertisingAPI()
        self.assertEqual(None, api.item_lookup('DEMOASIN02'))

        # check log output
        lc.check(
            ('price_monitor.product_advertising_api', 'ERROR', 'Lookup for item with ASIN DEMOASIN02 returned no product')
        )

    product_sample_ok = """
        <?xml version="1.0" ?>
        <itemlookupresponse xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
            <items>
                <request>
                    <isvalid>True</isvalid>
                    <itemlookuprequest>
                        <idtype>ASIN</idtype>
                        <itemid>DEMOASIN03</itemid>
                        <responsegroup>Large</responsegroup>
                        <variationpage>All</variationpage>
                    </itemlookuprequest>
                </request>
                <item>
                    <asin>DEMOASIN03</asin>
                    <itemattributes>
                        <title>Demo Series - Season 2 [Blu-ray]</title>
                        <binding>Blu-ray</binding>
                        <publicationdate>2014-12-22</publicationdate>
                        <releasedate>2014-12-22</releasedate>
                        <audiencerating>Freigegeben ab 16 Jahren</audiencerating>
                    </itemattributes>
                    <smallimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN03IMAGE._SL75_.jpg</url>
                        <height units="pixels">75</height>
                        <width units="pixels">59</width>
                    </smallimage>
                    <mediumimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN03IMAGE._SL160_.jpg</url>
                        <height units="pixels">160</height>
                        <width units="pixels">126</width>
                    </mediumimage>
                    <largeimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN03IMAGE.jpg</url>
                        <height units="pixels">500</height>
                        <width units="pixels">393</width>
                    </largeimage>
                    <offers>
                        <totaloffers>1</totaloffers>
                        <offer>
                            <offerlisting>
                                <price>
                                    <amount>1799</amount>
                                    <currencycode>EUR</currencycode>
                                    <formattedprice>EUR 17,99</formattedprice>
                                </price>
                            </offerlisting>
                        </offer>
                    </offers>
                </item>
            </items>
        </itemlookupresponse>
    """

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
        product_api_lookup.return_value = self.__get_product_bs(self.product_sample_ok)

        api = ProductAdvertisingAPI()
        values = api.item_lookup('DEMOASIN03')

        # ensure the mocks were called
        self.assertTrue(product_api_init.called)
        self.assertTrue(product_api_lookup.called)

        self.assertNotEqual(None, values)
        self.assertEqual(type(dict()), type(values))
        self.assertEqual(len(values), 14)

        self.assertEqual('DEMOASIN03', values['asin'])
        self.assertEqual('Demo Series - Season 2 [Blu-ray]', values['title'])
        self.assertEqual(None, values['isbn'])
        self.assertEqual(None, values['eisbn'])
        self.assertEqual('Blu-ray', values['binding'])
        self.assertEqual(datetime.datetime(2014, 12, 22), values['date_publication'])
        self.assertEqual(datetime.datetime(2014, 12, 22), values['date_release'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN03IMAGE.jpg', values['large_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN03IMAGE._SL160_.jpg', values['medium_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN03IMAGE._SL75_.jpg', values['small_image_url'])
        self.assertEqual('http://www.amazon.de/dp/DEMOASIN03/?tag=sample-assoc-tag', values['offer_url'])
        self.assertEqual(16, values['audience_rating'])
        self.assertEqual(17.99, values['price'])
        self.assertEqual('EUR', values['currency'])

        # check log output, should be empty
        lc.check()

    product_sample_no_price = """
        <?xml version="1.0" ?>
        <itemlookupresponse xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
            <items>
                <request>
                    <isvalid>True</isvalid>
                    <itemlookuprequest>
                        <idtype>ASIN</idtype>
                        <itemid>DEMOASIN04</itemid>
                        <responsegroup>Large</responsegroup>
                        <variationpage>All</variationpage>
                    </itemlookuprequest>
                </request>
                <item>
                    <asin>DEMOASIN04</asin>
                    <itemattributes>
                        <title>Another Demo Series - Season 1 (8 DVDs)</title>
                        <binding>DVD</binding>
                        <publicationdate>2004-11</publicationdate>
                        <releasedate>2004-10-27</releasedate>
                        <audiencerating>Freigegeben ab 16 Jahren</audiencerating>
                    </itemattributes>
                    <smallimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN04IMAGE._SL75_.jpg</url>
                        <height units="pixels">75</height>
                        <width units="pixels">59</width>
                    </smallimage>
                    <mediumimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN04IMAGE._SL160_.jpg</url>
                        <height units="pixels">160</height>
                        <width units="pixels">126</width>
                    </mediumimage>
                    <largeimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN04IMAGE.jpg</url>
                        <height units="pixels">500</height>
                        <width units="pixels">393</width>
                    </largeimage>
                    <offers>
                        <totaloffers>0</totaloffers>
                        <totalofferpages>0</totalofferpages>
                        <moreoffersurl>0</moreoffersurl>
                    </offers>
                </item>
            </items>
        </itemlookupresponse>
    """

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
        product_api_lookup.return_value = self.__get_product_bs(self.product_sample_no_price)

        api = ProductAdvertisingAPI()
        values = api.item_lookup('DEMOASIN04')

        # ensure the mocks were called
        self.assertTrue(product_api_init.called)
        self.assertTrue(product_api_lookup.called)

        self.assertNotEqual(None, values)
        self.assertEqual(type(dict()), type(values))
        self.assertEqual(len(values), 12)

        self.assertEqual('DEMOASIN04', values['asin'])
        self.assertEqual('Another Demo Series - Season 1 (8 DVDs)', values['title'])
        self.assertEqual(None, values['isbn'])
        self.assertEqual(None, values['eisbn'])
        self.assertEqual('DVD', values['binding'])
        # dateutil.parser.parse will find out the year and month of "2004-11" but as there is no day, the day is set to the current day
        self.assertEqual(datetime.datetime(2004, 11, datetime.datetime.now().day), values['date_publication'])
        self.assertEqual(datetime.datetime(2004, 10, 27), values['date_release'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN04IMAGE.jpg', values['large_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN04IMAGE._SL160_.jpg', values['medium_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/DEMOASIN04IMAGE._SL75_.jpg', values['small_image_url'])
        self.assertEqual('http://www.amazon.de/dp/DEMOASIN04/?tag=sample-assoc-tag', values['offer_url'])
        self.assertEqual(16, values['audience_rating'])

        # check log output, should be empty
        lc.check()

    product_sample_no_audience_rating = """
        <?xml version="1.0" ?>
        <itemlookupresponse xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
            <items>
                <request>
                    <isvalid>True</isvalid>
                    <itemlookuprequest>
                        <idtype>ASIN</idtype>
                        <itemid>123456789X</itemid>
                        <responsegroup>Large</responsegroup>
                        <variationpage>All</variationpage>
                    </itemlookuprequest>
                </request>
                <item>
                    <asin>123456789X</asin>
                    <itemattributes>
                        <title>A Sample Book</title>
                        <binding>Taschenbuch</binding>
                        <publicationdate>2014-08-18</publicationdate>
                        <releasedate>2014-08-18</releasedate>
                        <ean>9876543219876</ean>
                        <eanlist>
                            <eanlistelement>9876543219876</eanlistelement>
                        </eanlist>
                        <isbn>123456789X</isbn>
                    </itemattributes>
                    <smallimage>
                        <url>http://ecx.images-amazon.com/images/I/123456789XIMAGE._SL75_.jpg</url>
                        <height units="pixels">75</height>
                        <width units="pixels">59</width>
                    </smallimage>
                    <mediumimage>
                        <url>http://ecx.images-amazon.com/images/I/123456789XIMAGE._SL160_.jpg</url>
                        <height units="pixels">160</height>
                        <width units="pixels">126</width>
                    </mediumimage>
                    <largeimage>
                        <url>http://ecx.images-amazon.com/images/I/123456789XIMAGE.jpg</url>
                        <height units="pixels">500</height>
                        <width units="pixels">393</width>
                    </largeimage>
                    <offers>
                        <totaloffers>1</totaloffers>
                        <totalofferpages>1</totalofferpages>
                        <offer>
                            <offerattributes>
                                <condition>New</condition>
                            </offerattributes>
                            <offerlisting>
                                <offerlistingid>SAMPLEOFFERLISTINGID</offerlistingid>
                                <price>
                                    <amount>1000</amount>
                                    <currencycode>EUR</currencycode>
                                    <formattedprice>EUR 10,00</formattedprice>
                                </price>
                                <availability>Gewöhnlich versandfertig in 24 Stunden</availability>
                                <availabilityattributes>
                                    <availabilitytype>now</availabilitytype>
                                    <minimumhours>0</minimumhours>
                                    <maximumhours>0</maximumhours>
                                </availabilityattributes>
                                <iseligibleforsupersavershipping>1</iseligibleforsupersavershipping>
                            </offerlisting>
                        </offer>
                    </offers>
                </item>
            </items>
        </itemlookupresponse>
    """

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
        product_api_lookup.return_value = self.__get_product_bs(self.product_sample_no_audience_rating)

        api = ProductAdvertisingAPI()
        values = api.item_lookup('123456789X')

        # ensure the mocks were called
        # ensure the mocks were called
        self.assertTrue(product_api_init.called)
        self.assertTrue(product_api_lookup.called)

        self.assertNotEqual(None, values)
        self.assertEqual(type(dict()), type(values))
        self.assertEqual(len(values), 13)

        self.assertEqual('123456789X', values['asin'])
        self.assertEqual('A Sample Book', values['title'])
        self.assertEqual('123456789X', values['isbn'])
        self.assertEqual(None, values['eisbn'])
        self.assertEqual('Taschenbuch', values['binding'])
        self.assertEqual(datetime.datetime(2014, 8, 18), values['date_publication'])
        self.assertEqual(datetime.datetime(2014, 8, 18), values['date_release'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/123456789XIMAGE.jpg', values['large_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/123456789XIMAGE._SL160_.jpg', values['medium_image_url'])
        self.assertEqual('http://ecx.images-amazon.com/images/I/123456789XIMAGE._SL75_.jpg', values['small_image_url'])
        self.assertEqual('http://www.amazon.de/dp/123456789X/?tag=sample-assoc-tag', values['offer_url'])
        self.assertEqual(10.0, values['price'])
        self.assertEqual('EUR', values['currency'])

        # check log output, should be empty
        lc.check()
