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

product_sample_no_offers = """
<?xml version="1.0" ?>
<itemlookupresponse xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
    <items>
        <request>
            <isvalid>True</isvalid>
            <itemlookuprequest>
                <idtype>ASIN</idtype>
                <itemid>DEMOASIN05</itemid>
                <responsegroup>Large</responsegroup>
                <variationpage>All</variationpage>
            </itemlookuprequest>
        </request>
        <item>
            <asin>DEMOASIN05</asin>
            <itemattributes>
                <title>Sønderzeichen</title>
                <binding>Kindle Edition</binding>
                <publicationdate>2009-10-14</publicationdate>
                <releasedate>2009-10-14</releasedate>
            </itemattributes>
            <smallimage>
                <url>http://ecx.images-amazon.com/images/I/DEMOASIN05IMAGE._SL75_.jpg</url>
                <height units="pixels">75</height>
                <width units="pixels">59</width>
            </smallimage>
            <mediumimage>
                <url>http://ecx.images-amazon.com/images/I/DEMOASIN05IMAGE._SL160_.jpg</url>
                <height units="pixels">160</height>
                <width units="pixels">126</width>
            </mediumimage>
            <largeimage>
                <url>http://ecx.images-amazon.com/images/I/DEMOASIN05IMAGE.jpg</url>
                <height units="pixels">500</height>
                <width units="pixels">393</width>
            </largeimage>
        </item>
    </items>
</itemlookupresponse>
"""
