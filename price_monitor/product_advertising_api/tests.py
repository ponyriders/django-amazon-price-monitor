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
                        <itemid>DEMOASIN03</itemid>
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
                    <asin>DEMOASIN02</asin>
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
    def test_item_lookup_normal(self, papi_init, papi_lookup, lc):
        """
        Test for a normal bluray.
        :param papi_init: mockup for ProductAdvertisingAPI.__init__
        :type papi_init: unittest.mock.MagicMock
        :param papi_lookup: mockup for ProductAdvertisingAPI.lookup_at_amazon
        :type papi_init: unittest.mock.MagicMock
        :param lc: log capture instance
        :type lc: testfixtures.logcapture.LogCaptureForDecorator
        """
        papi_init.return_value = None
        papi_lookup.return_value = self.__get_product_bs(self.product_sample_ok)

        api = ProductAdvertisingAPI()
        values = api.item_lookup('DEMOASIN03')
        self.assertNotEqual(None, values)
        self.assertEqual(len(values), 14)

        # TODO test more

        self.assertTrue(papi_init.called)
        self.assertTrue(papi_lookup.called)

        # check log output, should be empty
        lc.check()

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
