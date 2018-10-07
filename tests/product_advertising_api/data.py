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

product_sample_no_images = """
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
            </smallimage>
            <mediumimage>
            </mediumimage>
            <largeimage>
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

product_sample_10_products = """
<html>
    <body>
        <itemlookupresponse xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
            <items>
                <request>
                    <isvalid>True</isvalid>
                    <itemlookuprequest>
                        <idtype>ASIN</idtype>
                        <itemid>DEMOASIN06</itemid>
                        <itemid>DEMOASIN07</itemid>
                        <itemid>DEMOASIN08</itemid>
                        <itemid>DEMOASIN09</itemid>
                        <itemid>DEMOASIN10</itemid>
                        <itemid>DEMOASIN11</itemid>
                        <itemid>DEMOASIN12</itemid>
                        <itemid>DEMOASIN13</itemid>
                        <itemid>DEMOASIN14</itemid>
                        <itemid>DEMOASIN15</itemid>
                        <responsegroup>Large</responsegroup>
                        <variationpage>All</variationpage>
                    </itemlookuprequest>
                </request>
                <item>
                    <asin>DEMOASIN06</asin>
                    <smallimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN06._SL75_.jpg</url>
                        <height units="pixels">75</height>
                        <width units="pixels">53</width>
                    </smallimage>
                    <mediumimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN06._SL160_.jpg</url>
                        <height units="pixels">160</height>
                        <width units="pixels">113</width>
                    </mediumimage>
                    <largeimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN06.jpg</url>
                        <height units="pixels">500</height>
                        <width units="pixels">354</width>
                    </largeimage>
                    <itemattributes>
                        <audiencerating>Freigegeben ab 12 Jahren</audiencerating>
                        <binding>DVD</binding>
                        <publicationdate>2012-10-05</publicationdate>
                        <releasedate>2008-11-07</releasedate>
                        <title>Hot Shots! - Teil 1 + Teil 2 [2 DVDs]</title>
                    </itemattributes>
                    <offers>
                        <totaloffers>1</totaloffers>
                        <offer>
                            <offerlisting>
                                <price>
                                    <amount>799</amount>
                                    <currencycode>EUR</currencycode>
                                </price>
                            </offerlisting>
                        </offer>
                    </offers>
                </item>
                <item>
                    <asin>DEMOASIN07</asin>
                    <smallimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN07._SL75_.jpg</url>
                        <height units="pixels">74</height>
                        <width units="pixels">75</width>
                    </smallimage>
                    <mediumimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN07._SL160_.jpg</url>
                        <height units="pixels">159</height>
                        <width units="pixels">160</width>
                    </mediumimage>
                    <largeimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN07.jpg</url>
                        <height units="pixels">496</height>
                        <width units="pixels">500</width>
                    </largeimage>
                    <itemattributes>
                        <binding>Audio CD</binding>
                        <releasedate>2004-06-14</releasedate>
                        <title>Greatest Hits</title>
                    </itemattributes>
                    <offers>
                        <totaloffers>1</totaloffers>
                        <offer>
                            <offerlisting>
                                <price>
                                    <amount>740</amount>
                                    <currencycode>EUR</currencycode>
                                </price>
                            </offerlisting>
                        </offer>
                    </offers>
                </item>
                <item>
                    <asin>DEMOASIN08</asin>
                    <smallimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN08._SL75_.jpg</url>
                        <height units="pixels">75</height>
                        <width units="pixels">75</width>
                    </smallimage>
                    <mediumimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN08._SL160_.jpg</url>
                        <height units="pixels">160</height>
                        <width units="pixels">160</width>
                    </mediumimage>
                    <largeimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN08.jpg</url>
                        <height units="pixels">500</height>
                        <width units="pixels">500</width>
                    </largeimage>
                    <itemattributes>
                        <binding>Audio CD</binding>
                        <publicationdate>2004-07-19</publicationdate>
                        <releasedate>2004-07-19</releasedate>
                        <title>Tyrannosaurus Hives</title>
                    </itemattributes>
                    <offers>
                        <totaloffers>1</totaloffers>
                        <offer>
                            <offerlisting>
                                <price>
                                    <amount>699</amount>
                                    <currencycode>EUR</currencycode>
                                </price>
                            </offerlisting>
                        </offer>
                    </offers>
                </item>
                <item>
                    <asin>DEMOASIN09</asin>
                    <smallimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN09._SL75_.jpg</url>
                        <height units="pixels">75</height>
                        <width units="pixels">53</width>
                    </smallimage>
                    <mediumimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN09._SL160_.jpg</url>
                        <height units="pixels">160</height>
                        <width units="pixels">113</width>
                    </mediumimage>
                    <largeimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN09.jpg</url>
                        <height units="pixels">475</height>
                        <width units="pixels">336</width>
                    </largeimage>
                    <itemattributes>
                        <audiencerating>Freigegeben ab 6 Jahren</audiencerating>
                        <binding>DVD</binding>
                        <releasedate>2004-08-01</releasedate>
                        <title>Moonlight &amp; Valentino</title>
                    </itemattributes>
                    <offers>
                        <totaloffers>1</totaloffers>
                        <offer>
                            <offerlisting>
                                <price>
                                    <amount>2297</amount>
                                    <currencycode>EUR</currencycode>
                                </price>
                            </offerlisting>
                        </offer>
                    </offers>
                </item>
                <item>
                    <asin>DEMOASIN10</asin>
                    <smallimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN10._SL75_.jpg</url>
                        <height units="pixels">75</height>
                        <width units="pixels">56</width>
                    </smallimage>
                    <mediumimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN10._SL160_.jpg</url>
                        <height units="pixels">160</height>
                        <width units="pixels">120</width>
                    </mediumimage>
                    <largeimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN10.jpg</url>
                        <height units="pixels">475</height>
                        <width units="pixels">356</width>
                    </largeimage>
                    <itemattributes>
                        <audiencerating>Freigegeben ab 16 Jahren</audiencerating>
                        <binding>DVD</binding>
                        <releasedate>2004-09-07</releasedate>
                        <title>Jeepers Creepers 1 &amp; 2 [Deluxe Edition] [4 DVDs]</title>
                    </itemattributes>
                    <offers>
                        <totaloffers>1</totaloffers>
                        <offer>
                            <offerlisting>
                                <price>
                                    <amount>1549</amount>
                                    <currencycode>EUR</currencycode>
                                </price>
                            </offerlisting>
                        </offer>
                    </offers>
                </item>
                <item>
                    <asin>DEMOASIN11</asin>
                    <smallimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN11._SL75_.jpg</url>
                        <height units="pixels">75</height>
                        <width units="pixels">75</width>
                    </smallimage>
                    <mediumimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN11._SL160_.jpg</url>
                        <height units="pixels">160</height>
                        <width units="pixels">160</width>
                    </mediumimage>
                    <largeimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN11.jpg</url>
                        <height units="pixels">500</height>
                        <width units="pixels">500</width>
                    </largeimage>
                    <itemattributes>
                        <binding>Audio CD</binding>
                        <publicationdate>2004-10-05</publicationdate>
                        <releasedate>2004-09-13</releasedate>
                        <title>Wintersun</title>
                    </itemattributes>
                    <offers>
                        <totaloffers>1</totaloffers>
                        <offer>
                            <offerlisting>
                                <price>
                                    <amount>2199</amount>
                                    <currencycode>EUR</currencycode>
                                </price>
                            </offerlisting>
                        </offer>
                    </offers>
                </item>
                <item>
                    <asin>DEMOASIN12</asin>
                    <smallimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN12._SL75_.jpg</url>
                        <height units="pixels">75</height>
                        <width units="pixels">56</width>
                    </smallimage>
                    <mediumimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN12._SL160_.jpg</url>
                        <height units="pixels">160</height>
                        <width units="pixels">120</width>
                    </mediumimage>
                    <largeimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN12.jpg</url>
                        <height units="pixels">475</height>
                        <width units="pixels">356</width>
                    </largeimage>
                    <itemattributes>
                        <audiencerating>Freigegeben ab 16 Jahren</audiencerating>
                        <binding>DVD</binding>
                        <publicationdate>2004-11</publicationdate>
                        <releasedate>2004-10-27</releasedate>
                        <title>Farscape - Season 1 (8 DVDs)</title>
                    </itemattributes>
                    <offers>
                        <totaloffers>1</totaloffers>
                        <offer>
                            <offerlisting>
                                <price>
                                    <amount>5999</amount>
                                    <currencycode>EUR</currencycode>
                                </price>
                            </offerlisting>
                        </offer>
                    </offers>
                </item>
                <item>
                    <asin>DEMOASIN13</asin>
                    <smallimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN13._SL75_.jpg</url>
                        <height units="pixels">75</height>
                        <width units="pixels">75</width>
                    </smallimage>
                    <mediumimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN13._SL160_.jpg</url>
                        <height units="pixels">160</height>
                        <width units="pixels">160</width>
                    </mediumimage>
                    <largeimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN13.jpg</url>
                        <height units="pixels">500</height>
                        <width units="pixels">500</width>
                    </largeimage>
                    <itemattributes>
                        <audiencerating>Freigegeben ohne Altersbeschränkung</audiencerating>
                        <binding>Audio CD</binding>
                        <releasedate>2005-01-21</releasedate>
                        <title>Hurricane Bar</title>
                    </itemattributes>
                    <offers>
                        <totaloffers>1</totaloffers>
                        <offer>
                            <offerlisting>
                                <price>
                                    <amount>499</amount>
                                    <currencycode>EUR</currencycode>
                                </price>
                            </offerlisting>
                        </offer>
                    </offers>
                </item>
                <item>
                    <asin>DEMOASIN14</asin>
                    <smallimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN14._SL75_.jpg</url>
                        <height units="pixels">75</height>
                        <width units="pixels">75</width>
                    </smallimage>
                    <mediumimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN14._SL160_.jpg</url>
                        <height units="pixels">160</height>
                        <width units="pixels">160</width>
                    </mediumimage>
                    <largeimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN14.jpg</url>
                        <height units="pixels">500</height>
                        <width units="pixels">500</width>
                    </largeimage>
                    <itemattributes>
                        <binding>Audio CD</binding>
                        <releasedate>2007-01-02</releasedate>
                        <title>Silent Alarm</title>
                    </itemattributes>
                    <offers>
                        <totaloffers>1</totaloffers>
                        <offer>
                            <offerlisting>
                                <price>
                                    <amount>1186</amount>
                                    <currencycode>EUR</currencycode>
                                </price>
                            </offerlisting>
                        </offer>
                    </offers>
                </item>
                <item>
                    <asin>DEMOASIN15</asin>
                    <smallimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN15._SL75_.jpg</url>
                        <height units="pixels">67</height>
                        <width units="pixels">75</width>
                    </smallimage>
                    <mediumimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN15._SL160_.jpg</url>
                        <height units="pixels">144</height>
                        <width units="pixels">160</width>
                    </mediumimage>
                    <largeimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN15.jpg</url>
                        <height units="pixels">449</height>
                        <width units="pixels">500</width>
                    </largeimage>
                    <itemattributes>
                        <binding>Audio CD</binding>
                        <publicationdate>2005</publicationdate>
                        <releasedate>2005-02-07</releasedate>
                        <title>Greatest Hits</title>
                    </itemattributes>
                    <offers>
                        <totaloffers>1</totaloffers>
                        <offer>
                            <offerlisting>
                                <price>
                                    <amount>899</amount>
                                    <currencycode>EUR</currencycode>
                                </price>
                            </offerlisting>
                        </offer>
                    </offers>
                </item>
            </items>
        </itemlookupresponse>
    </body>
</html>
"""


product_sample_3_products = """
<html>
    <body>
        <itemlookupresponse xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
            <items>
                <request>
                    <isvalid>True</isvalid>
                    <itemlookuprequest>
                        <idtype>ASIN</idtype>
                        <itemid>DEMOASIN16</itemid>
                        <itemid>DEMOASIN17</itemid>
                        <itemid>DEMOASIN18</itemid>
                        <responsegroup>Large</responsegroup>
                        <variationpage>All</variationpage>
                    </itemlookuprequest>
                </request>
                <item>
                    <asin>DEMOASIN16</asin>
                    <itemattributes>
                        <title>Another Demo Series - Season 1 (8 DVDs)</title>
                        <binding>DVD</binding>
                        <publicationdate>2004-11</publicationdate>
                        <releasedate>2004-10-27</releasedate>
                        <audiencerating>Freigegeben ab 16 Jahren</audiencerating>
                    </itemattributes>
                    <smallimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN16._SL75_.jpg</url>
                        <height units="pixels">75</height>
                        <width units="pixels">59</width>
                    </smallimage>
                    <mediumimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN16._SL160_.jpg</url>
                        <height units="pixels">160</height>
                        <width units="pixels">126</width>
                    </mediumimage>
                    <largeimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN16.jpg</url>
                        <height units="pixels">500</height>
                        <width units="pixels">393</width>
                    </largeimage>
                    <offers>
                        <totaloffers>0</totaloffers>
                        <totalofferpages>0</totalofferpages>
                        <moreoffersurl>0</moreoffersurl>
                    </offers>
                </item>
                <item>
                    <asin>DEMOASIN17</asin>
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
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN17._SL75_.jpg</url>
                        <height units="pixels">75</height>
                        <width units="pixels">59</width>
                    </smallimage>
                    <mediumimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN17._SL160_.jpg</url>
                        <height units="pixels">160</height>
                        <width units="pixels">126</width>
                    </mediumimage>
                    <largeimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN17.jpg</url>
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
                <item>
                    <asin>DEMOASIN18</asin>
                    <itemattributes>
                        <title>Sønderzeichen</title>
                        <binding>Kindle Edition</binding>
                        <publicationdate>2009-10-14</publicationdate>
                        <releasedate>2009-10-14</releasedate>
                    </itemattributes>
                    <smallimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN18._SL75_.jpg</url>
                        <height units="pixels">75</height>
                        <width units="pixels">59</width>
                    </smallimage>
                    <mediumimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN18._SL160_.jpg</url>
                        <height units="pixels">160</height>
                        <width units="pixels">126</width>
                    </mediumimage>
                    <largeimage>
                        <url>http://ecx.images-amazon.com/images/I/DEMOASIN18.jpg</url>
                        <height units="pixels">500</height>
                        <width units="pixels">393</width>
                    </largeimage>
                </item>
            </items>
        </itemlookupresponse>
    </body>
</html>
"""

product_sample_with_artist = """
<itemlookupresponse xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
    <items>
        <request>
            <isvalid>True</isvalid>
            <itemlookuprequest>
                <idtype>ASIN</idtype>
                <itemid>DEMOASIN19</itemid>
                <responsegroup>Large</responsegroup>
                <variationpage>All</variationpage>
            </itemlookuprequest>
        </request>
        <item>
            <asin>DEMOASIN19</asin>
            <smallimage>
                <url>http://ecx.images-amazon.com/images/I/DEMOASIN19._SL75_.jpg</url>
                <height units="pixels">75</height>
                <width units="pixels">75</width>
            </smallimage>
            <mediumimage>
                <url>http://ecx.images-amazon.com/images/I/DEMOASIN19._SL160_.jpg</url>
                <height units="pixels">160</height>
                <width units="pixels">160</width>
            </mediumimage>
            <largeimage>
                <url>http://ecx.images-amazon.com/images/I/DEMOASIN19.jpg</url>
                <height units="pixels">500</height>
                <width units="pixels">500</width>
            </largeimage>
            <itemattributes>
                <artist>The Artist</artist>
                <binding>Audio CD</binding>
                <brand>SOME BRAND</brand>
                <feature>CD Album</feature>
                <feature>herausgegeben 2015 in Europa von SOME BRAND (SOMEBRAND123)</feature>
                <feature>Musikstil: Rock / Alternative Rock</feature>
                <format>CD</format>
                <itemdimensions>
                    <height units="hundredths-inches">50</height>
                    <length units="hundredths-inches">500</length>
                    <width units="hundredths-inches">550</width>
                </itemdimensions>
                <label>SOME BRAND (SOME COMPANY)</label>
                <languages>
                    <language>
                        <name>Englisch</name>
                        <type>Unbekannt</type>
                    </language>
                </languages>
                <manufacturer>SOME BRAND (SOME COMPANY)</manufacturer>
                <mpn>SBR1234567</mpn>
                <numberofdiscs>1</numberofdiscs>
                <numberofitems>1</numberofitems>
                <packagedimensions>
                    <height units="hundredths-inches">31</height>
                    <length units="hundredths-inches">551</length>
                    <weight units="hundredths-pounds">18</weight>
                    <width units="hundredths-inches">512</width>
                </packagedimensions>
                <packagequantity>1</packagequantity>
                <partnumber>SBR1234567</partnumber>
                <productgroup>Music</productgroup>
                <producttypename>SOME BRAND (SOME COMPANY)</producttypename>
                <publicationdate>2015</publicationdate>
                <publisher>SOME BRAND (SOME COMPANY)</publisher>
                <releasedate>2015-02-27</releasedate>
                <studio>SOME BRAND (SOME COMPANY)</studio>
                <title>The CD Title</title>
                <upc>1234567879012</upc>
                <upclist>
                    <upclistelement>1234567879012</upclistelement>
                </upclist>
            </itemattributes>
            <offersummary>
                <lowestnewprice>
                    <amount>747</amount>
                    <currencycode>EUR</currencycode>
                    <formattedprice>EUR 7,47</formattedprice>
                </lowestnewprice>
                <lowestusedprice>
                    <amount>901</amount>
                    <currencycode>EUR</currencycode>
                    <formattedprice>EUR 9,01</formattedprice>
                </lowestusedprice>
                <totalnew>94</totalnew>
                <totalused>3</totalused>
                <totalcollectible>0</totalcollectible>
                <totalrefurbished>0</totalrefurbished>
            </offersummary>
            <offers>
                <totaloffers>1</totaloffers>
                <totalofferpages>1</totalofferpages>
                <offer>
                    <offerattributes>
                        <condition>New</condition>
                    </offerattributes>
                    <offerlisting>
                        <offerlistingid>SAMPELOFFERLISTINGID</offerlistingid>
                        <price>
                            <amount>1299</amount>
                            <currencycode>EUR</currencycode>
                            <formattedprice>EUR 12,99</formattedprice>
                        </price>
                        <availability>Gewöhnlich versandfertig in 24 Stunden</availability>
                        <availabilityattributes>
                            <availabilitytype>now</availabilitytype>
                            <minimumhours>0</minimumhours>
                            <maximumhours>0</maximumhours>
                        </availabilityattributes>
                        <iseligibleforsupersavershipping>1</iseligibleforsupersavershipping>
                        <iseligibleforprime>1</iseligibleforprime>
                    </offerlisting>
                </offer>
            </offers>
            <tracks>
                <disc number="1">
                    <track number="1">Title 1</track>
                    <track number="2">Title 2</track>
                    <track number="3">Title 3</track>
                    <track number="4">Title 4</track>
                    <track number="5">Title 5</track>
                </disc>
            </tracks>
        </item>
    </items>
</itemlookupresponse>
"""

# a product with an ISBN-13 in the ISBN-10 field, see issue https://github.com/ponyriders/django-amazon-price-monitor/issues/121
product_sample_isbn_issue = """
<itemlookupresponse xmlns="http://webservices.amazon.com/AWSECommerceService/2013-08-01">
    <items>
        <request>
            <isvalid>True</isvalid>
            <itemlookuprequest>
                <idtype>ASIN</idtype>
                <itemid>TESTASIN20</itemid>
                <responsegroup>Large</responsegroup>
                <variationpage>All</variationpage>
            </itemlookuprequest>
        </request>
        <item>
            <asin>TESTASIN20</asin>
            <salesrank>2</salesrank>
            <smallimage>
                <url>http://ecx.images-amazon.com/images/I/TESTASIN20._SL75_.jpg</url>
                <height units="pixels">75</height>
                <width units="pixels">75</width>
            </smallimage>
            <mediumimage>
                <url>http://ecx.images-amazon.com/images/I/TESTASIN20._SL160_.jpg</url>
                <height units="pixels">160</height>
                <width units="pixels">160</width>
            </mediumimage>
            <largeimage>
                <url>http://ecx.images-amazon.com/images/I/TESTASIN20.jpg</url>
                <height units="pixels">500</height>
                <width units="pixels">500</width>
            </largeimage>
            <itemattributes>
                <actor>John Doe</actor>
                <actor>Jane Doe</actor>
                <aspectratio>2.39:1</aspectratio>
                <audiencerating>Freigegeben ab 16 Jahren</audiencerating>
                <binding>Blu-ray</binding>
                <brand>Test Distribution Company</brand>
                <creator role="Hauptdarsteller">John Doe</creator>
                <creator role="Hauptdarsteller">Jane Doe</creator>
                <director>John Director</director>
                <ean>1234567890123</ean>
                <eanlist>
                    <eanlistelement>1234567890123</eanlistelement>
                </eanlist>
                <edition>Standard Edition</edition>
                <format>Letterboxed</format>
                <format>Widescreen</format>
                <isbn>1234567890123</isbn>
                <label>Test Label Company</label>
                <manufacturer>Test Manufacturer Company</manufacturer>
                <mpn>12345678</mpn>
                <numberofdiscs>2</numberofdiscs>
                <numberofitems>2</numberofitems>
                <packagedimensions>
                    <height units="Hundertstel Zoll">39</height>
                    <length units="Hundertstel Zoll">669</length>
                    <weight units="Hundertstel Pfund">18</weight>
                    <width units="Hundertstel Zoll">528</width>
                </packagedimensions>
                <partnumber>12345678</partnumber>
                <productgroup>DVD &amp; Blu-ray</productgroup>
                <producttypename>ABIS_BOOK</producttypename>
                <publicationdate>2018-09-27</publicationdate>
                <publisher>Test Publisher Company</publisher>
                <regioncode>2</regioncode>
                <releasedate>2018-09-27</releasedate>
                <runningtime units="Minuten">119</runningtime>
                <studio>Test Studio Company</studio>
                <title>The ISDN Test Product</title>
            </itemattributes>
        </item>
    </items>
</itemlookupresponse>
"""
