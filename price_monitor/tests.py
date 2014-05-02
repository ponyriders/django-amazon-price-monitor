import unittest

from .models import Product

from lxml import objectify

from amazon.api import AmazonProduct


class ProductTest(unittest.TestCase):

    # General XML, structure taken from a Blu-Ray, I replaced the ASIN, titles and descriptions, assoc tag, image identifiers, and more
    # ASIN: X100Y200WZ
    # assoc-tag: sample-assoc-tag
    test_xml = """
        <Item xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
            <ASIN>X100Y200WZ</ASIN>
            <DetailPageURL>
                http://www.amazon.de/Sample-Product-Title-Blu-ray/dp/X100Y200WZ%3FSubscriptionId%3DXXXXXXXXXXXXXXX0XXXX%26tag%3Dsample-assoc-tag%26linkCode%3Dxm2%26camp%3D2025%26creative%3D165953%26creativeASIN%3DX100Y200WZ
            </DetailPageURL>
            <ItemLinks>
                <ItemLink>
                    <Description>Add To Wishlist</Description>
                    <URL>
                        http://www.amazon.de/gp/registry/wishlist/add-item.html%3Fasin.0%3DX100Y200WZ%26SubscriptionId%3DXXXXXXXXXXXXXXX0XXXX%26tag%3Dsample-assoc-tag%26linkCode%3Dxm2%26camp%3D2025%26creative%3D12738%26creativeASIN%3DX100Y200WZ
                    </URL>
                </ItemLink>
                <ItemLink>
                    <Description>Tell A Friend</Description>
                    <URL>
                        http://www.amazon.de/gp/pdp/taf/X100Y200WZ%3FSubscriptionId%3DXXXXXXXXXXXXXXX0XXXX%26tag%3Dsample-assoc-tag%26linkCode%3Dxm2%26camp%3D2025%26creative%3D12738%26creativeASIN%3DX100Y200WZ
                    </URL>
                </ItemLink>
                <ItemLink>
                    <Description>All Customer Reviews</Description>
                    <URL>
                        http://www.amazon.de/review/product/X100Y200WZ%3FSubscriptionId%3DXXXXXXXXXXXXXXX0XXXX%26tag%3Dsample-assoc-tag%26linkCode%3Dxm2%26camp%3D2025%26creative%3D12738%26creativeASIN%3DX100Y200WZ
                    </URL>
                </ItemLink>
                <ItemLink>
                    <Description>All Offers</Description>
                    <URL>
                        http://www.amazon.de/gp/offer-listing/X100Y200WZ%3FSubscriptionId%3DXXXXXXXXXXXXXXX0XXXX%26tag%3Dsample-assoc-tag%26linkCode%3Dxm2%26camp%3D2025%26creative%3D12738%26creativeASIN%3DX100Y200WZ
                    </URL>
                </ItemLink>
            </ItemLinks>
            <SalesRank>247</SalesRank>
            <SmallImage>
                <URL>http://ecx.images-amazon.com/images/I/99xXxxxX9XL._SL75_.jpg</URL>
                <Height Units="pixels">75</Height>
                <Width Units="pixels">61</Width>
            </SmallImage>
            <MediumImage>
                <URL>http://ecx.images-amazon.com/images/I/99xXxxxX9XL._SL160_.jpg</URL>
                <Height Units="pixels">160</Height>
                <Width Units="pixels">129</Width>
            </MediumImage>
            <LargeImage>
                <URL>http://ecx.images-amazon.com/images/I/99xXxxxX9XL.jpg</URL>
                <Height Units="pixels">500</Height>
                <Width Units="pixels">404</Width>
            </LargeImage>
            <ImageSets>
                <ImageSet Category="primary">
                    <SwatchImage>
                        <URL>http://ecx.images-amazon.com/images/I/99xXxxxX9XL._SL30_.jpg</URL>
                        <Height Units="pixels">30</Height>
                        <Width Units="pixels">24</Width>
                    </SwatchImage>
                    <SmallImage>
                        <URL>http://ecx.images-amazon.com/images/I/99xXxxxX9XL._SL75_.jpg</URL>
                        <Height Units="pixels">75</Height>
                        <Width Units="pixels">61</Width>
                    </SmallImage>
                    <ThumbnailImage>
                        <URL>http://ecx.images-amazon.com/images/I/99xXxxxX9XL._SL75_.jpg</URL>
                        <Height Units="pixels">75</Height>
                        <Width Units="pixels">61</Width>
                    </ThumbnailImage>
                    <TinyImage>
                        <URL>http://ecx.images-amazon.com/images/I/99xXxxxX9XL._SL110_.jpg</URL>
                        <Height Units="pixels">110</Height>
                        <Width Units="pixels">89</Width>
                    </TinyImage>
                    <MediumImage>
                        <URL>http://ecx.images-amazon.com/images/I/99xXxxxX9XL._SL160_.jpg</URL>
                        <Height Units="pixels">160</Height>
                        <Width Units="pixels">129</Width>
                    </MediumImage>
                    <LargeImage>
                        <URL>http://ecx.images-amazon.com/images/I/99xXxxxX9XL.jpg</URL>
                        <Height Units="pixels">500</Height>
                        <Width Units="pixels">404</Width>
                    </LargeImage>
                </ImageSet>
                <ImageSet Category="variant">
                    <SwatchImage>
                        <URL>http://ecx.images-amazon.com/images/I/41kCUr1qiML._SL30_.jpg</URL>
                        <Height Units="pixels">20</Height>
                        <Width Units="pixels">30</Width>
                    </SwatchImage>
                    <SmallImage>
                        <URL>http://ecx.images-amazon.com/images/I/41kCUr1qiML._SL75_.jpg</URL>
                        <Height Units="pixels">50</Height>
                        <Width Units="pixels">75</Width>
                    </SmallImage>
                    <ThumbnailImage>
                        <URL>http://ecx.images-amazon.com/images/I/41kCUr1qiML._SL75_.jpg</URL>
                        <Height Units="pixels">50</Height>
                        <Width Units="pixels">75</Width>
                    </ThumbnailImage>
                    <TinyImage>
                        <URL>http://ecx.images-amazon.com/images/I/41kCUr1qiML._SL110_.jpg</URL>
                        <Height Units="pixels">73</Height>
                        <Width Units="pixels">110</Width>
                    </TinyImage>
                    <MediumImage>
                        <URL>http://ecx.images-amazon.com/images/I/41kCUr1qiML._SL160_.jpg</URL>
                        <Height Units="pixels">107</Height>
                        <Width Units="pixels">160</Width>
                    </MediumImage>
                    <LargeImage>
                        <URL>http://ecx.images-amazon.com/images/I/41kCUr1qiML.jpg</URL>
                        <Height Units="pixels">334</Height>
                        <Width Units="pixels">500</Width>
                    </LargeImage>
                </ImageSet>
                <ImageSet Category="variant">
                    <SwatchImage>
                        <URL>http://ecx.images-amazon.com/images/I/41chfBf9lkL._SL30_.jpg</URL>
                        <Height Units="pixels">22</Height>
                        <Width Units="pixels">30</Width>
                    </SwatchImage>
                    <SmallImage>
                        <URL>http://ecx.images-amazon.com/images/I/41chfBf9lkL._SL75_.jpg</URL>
                        <Height Units="pixels">56</Height>
                        <Width Units="pixels">75</Width>
                    </SmallImage>
                    <ThumbnailImage>
                        <URL>http://ecx.images-amazon.com/images/I/41chfBf9lkL._SL75_.jpg</URL>
                        <Height Units="pixels">56</Height>
                        <Width Units="pixels">75</Width>
                    </ThumbnailImage>
                    <TinyImage>
                        <URL>http://ecx.images-amazon.com/images/I/41chfBf9lkL._SL110_.jpg</URL>
                        <Height Units="pixels">82</Height>
                        <Width Units="pixels">110</Width>
                    </TinyImage>
                    <MediumImage>
                        <URL>http://ecx.images-amazon.com/images/I/41chfBf9lkL._SL160_.jpg</URL>
                        <Height Units="pixels">120</Height>
                        <Width Units="pixels">160</Width>
                    </MediumImage>
                    <LargeImage>
                        <URL>http://ecx.images-amazon.com/images/I/41chfBf9lkL.jpg</URL>
                        <Height Units="pixels">375</Height>
                        <Width Units="pixels">500</Width>
                    </LargeImage>
                </ImageSet>
                <ImageSet Category="variant">
                    <SwatchImage>
                        <URL>http://ecx.images-amazon.com/images/I/51kAx1j7IFL._SL30_.jpg</URL>
                        <Height Units="pixels">20</Height>
                        <Width Units="pixels">30</Width>
                    </SwatchImage>
                    <SmallImage>
                        <URL>http://ecx.images-amazon.com/images/I/51kAx1j7IFL._SL75_.jpg</URL>
                        <Height Units="pixels">50</Height>
                        <Width Units="pixels">75</Width>
                    </SmallImage>
                    <ThumbnailImage>
                        <URL>http://ecx.images-amazon.com/images/I/51kAx1j7IFL._SL75_.jpg</URL>
                        <Height Units="pixels">50</Height>
                        <Width Units="pixels">75</Width>
                    </ThumbnailImage>
                    <TinyImage>
                        <URL>http://ecx.images-amazon.com/images/I/51kAx1j7IFL._SL110_.jpg</URL>
                        <Height Units="pixels">73</Height>
                        <Width Units="pixels">110</Width>
                    </TinyImage>
                    <MediumImage>
                        <URL>http://ecx.images-amazon.com/images/I/51kAx1j7IFL._SL160_.jpg</URL>
                        <Height Units="pixels">107</Height>
                        <Width Units="pixels">160</Width>
                    </MediumImage>
                    <LargeImage>
                        <URL>http://ecx.images-amazon.com/images/I/51kAx1j7IFL.jpg</URL>
                        <Height Units="pixels">334</Height>
                        <Width Units="pixels">500</Width>
                    </LargeImage>
                </ImageSet>
                <ImageSet Category="variant">
                    <SwatchImage>
                        <URL>http://ecx.images-amazon.com/images/I/61j2n3K2I7L._SL30_.jpg</URL>
                        <Height Units="pixels">20</Height>
                        <Width Units="pixels">30</Width>
                    </SwatchImage>
                    <SmallImage>
                        <URL>http://ecx.images-amazon.com/images/I/61j2n3K2I7L._SL75_.jpg</URL>
                        <Height Units="pixels">50</Height>
                        <Width Units="pixels">75</Width>
                    </SmallImage>
                    <ThumbnailImage>
                        <URL>http://ecx.images-amazon.com/images/I/61j2n3K2I7L._SL75_.jpg</URL>
                        <Height Units="pixels">50</Height>
                        <Width Units="pixels">75</Width>
                    </ThumbnailImage>
                    <TinyImage>
                        <URL>http://ecx.images-amazon.com/images/I/61j2n3K2I7L._SL110_.jpg</URL>
                        <Height Units="pixels">73</Height>
                        <Width Units="pixels">110</Width>
                    </TinyImage>
                    <MediumImage>
                        <URL>http://ecx.images-amazon.com/images/I/61j2n3K2I7L._SL160_.jpg</URL>
                        <Height Units="pixels">107</Height>
                        <Width Units="pixels">160</Width>
                    </MediumImage>
                    <LargeImage>
                        <URL>http://ecx.images-amazon.com/images/I/61j2n3K2I7L.jpg</URL>
                        <Height Units="pixels">334</Height>
                        <Width Units="pixels">500</Width>
                    </LargeImage>
                </ImageSet>
                <ImageSet Category="variant">
                    <SwatchImage>
                        <URL>http://ecx.images-amazon.com/images/I/41oIf-%2BDAAL._SL30_.jpg</URL>
                        <Height Units="pixels">20</Height>
                        <Width Units="pixels">30</Width>
                    </SwatchImage>
                    <SmallImage>
                        <URL>http://ecx.images-amazon.com/images/I/41oIf-%2BDAAL._SL75_.jpg</URL>
                        <Height Units="pixels">50</Height>
                        <Width Units="pixels">75</Width>
                    </SmallImage>
                    <ThumbnailImage>
                        <URL>http://ecx.images-amazon.com/images/I/41oIf-%2BDAAL._SL75_.jpg</URL>
                        <Height Units="pixels">50</Height>
                        <Width Units="pixels">75</Width>
                    </ThumbnailImage>
                    <TinyImage>
                        <URL>http://ecx.images-amazon.com/images/I/41oIf-%2BDAAL._SL110_.jpg</URL>
                        <Height Units="pixels">73</Height>
                        <Width Units="pixels">110</Width>
                    </TinyImage>
                    <MediumImage>
                        <URL>http://ecx.images-amazon.com/images/I/41oIf-%2BDAAL._SL160_.jpg</URL>
                        <Height Units="pixels">107</Height>
                        <Width Units="pixels">160</Width>
                    </MediumImage>
                    <LargeImage>
                        <URL>http://ecx.images-amazon.com/images/I/41oIf-%2BDAAL.jpg</URL>
                        <Height Units="pixels">334</Height>
                        <Width Units="pixels">500</Width>
                    </LargeImage>
                </ImageSet>
                <ImageSet Category="variant">
                    <SwatchImage>
                        <URL>http://ecx.images-amazon.com/images/I/51hlK0wnleL._SL30_.jpg</URL>
                        <Height Units="pixels">20</Height>
                        <Width Units="pixels">30</Width>
                    </SwatchImage>
                    <SmallImage>
                        <URL>http://ecx.images-amazon.com/images/I/51hlK0wnleL._SL75_.jpg</URL>
                        <Height Units="pixels">50</Height>
                        <Width Units="pixels">75</Width>
                    </SmallImage>
                    <ThumbnailImage>
                        <URL>http://ecx.images-amazon.com/images/I/51hlK0wnleL._SL75_.jpg</URL>
                        <Height Units="pixels">50</Height>
                        <Width Units="pixels">75</Width>
                    </ThumbnailImage>
                    <TinyImage>
                        <URL>http://ecx.images-amazon.com/images/I/51hlK0wnleL._SL110_.jpg</URL>
                        <Height Units="pixels">73</Height>
                        <Width Units="pixels">110</Width>
                    </TinyImage>
                    <MediumImage>
                        <URL>http://ecx.images-amazon.com/images/I/51hlK0wnleL._SL160_.jpg</URL>
                        <Height Units="pixels">107</Height>
                        <Width Units="pixels">160</Width>
                    </MediumImage>
                    <LargeImage>
                        <URL>http://ecx.images-amazon.com/images/I/51hlK0wnleL.jpg</URL>
                        <Height Units="pixels">334</Height>
                        <Width Units="pixels">500</Width>
                    </LargeImage>
                </ImageSet>
                <ImageSet Category="variant">
                    <SwatchImage>
                        <URL>http://ecx.images-amazon.com/images/I/51tB7iCLcDL._SL30_.jpg</URL>
                        <Height Units="pixels">20</Height>
                        <Width Units="pixels">30</Width>
                    </SwatchImage>
                    <SmallImage>
                        <URL>http://ecx.images-amazon.com/images/I/51tB7iCLcDL._SL75_.jpg</URL>
                        <Height Units="pixels">50</Height>
                        <Width Units="pixels">75</Width>
                    </SmallImage>
                    <ThumbnailImage>
                        <URL>http://ecx.images-amazon.com/images/I/51tB7iCLcDL._SL75_.jpg</URL>
                        <Height Units="pixels">50</Height>
                        <Width Units="pixels">75</Width>
                    </ThumbnailImage>
                    <TinyImage>
                        <URL>http://ecx.images-amazon.com/images/I/51tB7iCLcDL._SL110_.jpg</URL>
                        <Height Units="pixels">73</Height>
                        <Width Units="pixels">110</Width>
                    </TinyImage>
                    <MediumImage>
                        <URL>http://ecx.images-amazon.com/images/I/51tB7iCLcDL._SL160_.jpg</URL>
                        <Height Units="pixels">107</Height>
                        <Width Units="pixels">160</Width>
                    </MediumImage>
                    <LargeImage>
                        <URL>http://ecx.images-amazon.com/images/I/51tB7iCLcDL.jpg</URL>
                        <Height Units="pixels">333</Height>
                        <Width Units="pixels">500</Width>
                    </LargeImage>
                </ImageSet>
            </ImageSets>
            <ItemAttributes>
                <Actor>John Doe</Actor>
                <Actor>Jane Doe</Actor>
                <Actor>Mike Whatever</Actor>
                <Actor>Irene Sample</Actor>
                <Actor>Max Mustermann</Actor>
                <AspectRatio>16:9 - 1.77:1</AspectRatio>
                <AudienceRating>Freigegeben ab 16 Jahren</AudienceRating>
                <Binding>Blu-ray</Binding>
                <Brand>Sample Brand Company</Brand>
                <Creator Role="Hauptdarsteller">John Doe</Creator>
                <Creator Role="Hauptdarsteller">Jane Doe</Creator>
                <EAN>0000000000000</EAN>
                <EANList>
                    <EANListElement>0000000000000</EANListElement>
                </EANList>
                <Format>Blu-ray</Format>
                <IsEligibleForTradeIn>1</IsEligibleForTradeIn>
                <ItemDimensions>
                    <Height Units="hundredths-inches">39</Height>
                    <Length Units="hundredths-inches">39</Length>
                    <Width Units="hundredths-inches">39</Width>
                </ItemDimensions>
                <Label>Sample Label Company</Label>
                <Languages>
                    <Language>
                        <Name>Deutsch</Name>
                        <Type>Subtitled</Type>
                    </Language>
                    <Language>
                        <Name>Englisch</Name>
                        <Type>Subtitled</Type>
                    </Language>
                    <Language>
                        <Name>T&#252;rkisch</Name>
                        <Type>Subtitled</Type>
                    </Language>
                    <Language>
                        <Name>Deutsch</Name>
                        <Type>Original</Type>
                        <AudioFormat>Dolby Digital 5.1</AudioFormat>
                    </Language>
                    <Language>
                        <Name>Englisch</Name>
                        <Type>Original</Type>
                        <AudioFormat>DTS-HD 5.1</AudioFormat>
                    </Language>
                    <Language>
                        <Name>Englisch</Name>
                        <Type>Published</Type>
                        <AudioFormat>DTS-HD 5.1</AudioFormat>
                    </Language>
                    <Language>
                        <Name>Deutsch</Name>
                        <Type>Published</Type>
                        <AudioFormat>Dolby Digital 5.1</AudioFormat>
                    </Language>
                </Languages>
                <ListPrice>
                    <Amount>3499</Amount>
                    <CurrencyCode>EUR</CurrencyCode>
                    <FormattedPrice>EUR 34,99</FormattedPrice>
                </ListPrice>
                <Manufacturer>Sample Manufacturer Company</Manufacturer>
                <MPN>000000</MPN>
                <NumberOfItems>2</NumberOfItems>
                <PackageDimensions>
                    <Height Units="hundredths-inches">55</Height>
                    <Length Units="hundredths-inches">677</Length>
                    <Weight Units="hundredths-pounds">31</Weight>
                    <Width Units="hundredths-inches">543</Width>
                </PackageDimensions>
                <PartNumber>000000</PartNumber>
                <ProductGroup>DVD &amp; Blu-ray</ProductGroup>
                <ProductTypeName>ABIS_DVD</ProductTypeName>
                <Publisher>Sample Publisher Company</Publisher>
                <ReleaseDate>1970-01-01</ReleaseDate>
                <RunningTime Units="Minuten">391</RunningTime>
                <Studio>Sample Studio Company</Studio>
                <Title>Sample Product Title [Blu-ray]</Title>
                <TradeInValue>
                    <Amount>1160</Amount>
                    <CurrencyCode>EUR</CurrencyCode>
                    <FormattedPrice>EUR 11,60</FormattedPrice>
                </TradeInValue>
            </ItemAttributes>
            <OfferSummary>
                <LowestNewPrice>
                    <Amount>2299</Amount>
                    <CurrencyCode>EUR</CurrencyCode>
                    <FormattedPrice>EUR 22,99</FormattedPrice>
                </LowestNewPrice>
                <LowestUsedPrice>
                    <Amount>1899</Amount>
                    <CurrencyCode>EUR</CurrencyCode>
                    <FormattedPrice>EUR 18,99</FormattedPrice>
                </LowestUsedPrice>
                <LowestCollectiblePrice>
                    <Amount>2899</Amount>
                    <CurrencyCode>EUR</CurrencyCode>
                    <FormattedPrice>EUR 28,99</FormattedPrice>
                </LowestCollectiblePrice>
                <TotalNew>31</TotalNew>
                <TotalUsed>2</TotalUsed>
                <TotalCollectible>1</TotalCollectible>
                <TotalRefurbished>0</TotalRefurbished>
            </OfferSummary>
            <Offers>
                <TotalOffers>1</TotalOffers>
                <TotalOfferPages>1</TotalOfferPages>
                <MoreOffersUrl>
                    http://www.amazon.de/gp/offer-listing/X100Y200WZ%3FSubscriptionId%3DXXXXXXXXXXXXXXX0XXXX%26tag%3Dsample-assoc-tag%26linkCode%3Dxm2%26camp%3D2025%26creative%3D12738%26creativeASIN%3DX100Y200WZ
                </MoreOffersUrl>
                <Offer>
                    <OfferAttributes>
                        <Condition>New</Condition>
                    </OfferAttributes>
                    <OfferListing>
                        <OfferListingId>I8bZir9PekJsapBzvyyknNOXXXnUUfx%2FiGFRyTSYLV7pSeSTfmQffX%2Bt1UwZpgNA4DJ5fK88xjuW9qjzVlma7of06k6UWs2cfUM4kMKM7xY%3D
                        </OfferListingId>
                        <Price>
                            <Amount>2299</Amount>
                            <CurrencyCode>EUR</CurrencyCode>
                            <FormattedPrice>EUR 22,99</FormattedPrice>
                        </Price>
                        <AmountSaved>
                            <Amount>1200</Amount>
                            <CurrencyCode>EUR</CurrencyCode>
                            <FormattedPrice>EUR 12,00</FormattedPrice>
                        </AmountSaved>
                        <PercentageSaved>34</PercentageSaved>
                        <Availability>Gew&#246;hnlich versandfertig in 24 Stunden</Availability>
                        <AvailabilityAttributes>
                            <AvailabilityType>now</AvailabilityType>
                            <MinimumHours>0</MinimumHours>
                            <MaximumHours>0</MaximumHours>
                        </AvailabilityAttributes>
                        <IsEligibleForSuperSaverShipping>1</IsEligibleForSuperSaverShipping>
                    </OfferListing>
                </Offer>
            </Offers>
            <CustomerReviews>
                <IFrameURL>http://www.amazon.de/reviews/iframe?akid=XXXXXXXXXXXXXXX0XXXX&amp;alinkCode=xm2&amp;asin=X100Y200WZ&amp;atag=sample-assoc-tag&amp;exp=2014-05-03T10%3A11%3A14Z&amp;v=2&amp;sig=%2BPm8JeyplMrWqCt%2FhENkZBSJ7gxasPr8%2Ft6RKf9tYg8%3D</IFrameURL>
                <HasReviews>true</HasReviews>
            </CustomerReviews>
            <EditorialReviews>
                <EditorialReview>
                    <Source>Product Description</Source>
                    <Content>Besonderheiten: Freigegeben ab 16 Jahre</Content>
                    <IsLinkSuppressed>0</IsLinkSuppressed>
                </EditorialReview>
                <EditorialReview>
                    <Source>Kurzbeschreibung</Source>
                    <Content>Lorem ipsum dolor irgendwas blabla.</Content>
                    <IsLinkSuppressed>0</IsLinkSuppressed>
                </EditorialReview>
            </EditorialReviews>
            <SimilarProducts>
                <SimilarProduct>
                    <ASIN>X100Y200W0</ASIN>
                    <Title>Similar Product 0 [Blu-ray]</Title>
                </SimilarProduct>
                <SimilarProduct>
                    <ASIN>X100Y200W1</ASIN>
                    <Title>Similar Product 1 [Blu-ray]</Title>
                </SimilarProduct>
                <SimilarProduct>
                    <ASIN>X100Y200W2</ASIN>
                    <Title>Similar Product 2 [Blu-ray]</Title>
                </SimilarProduct>
                <SimilarProduct>
                    <ASIN>X100Y200W3</ASIN>
                    <Title>Similar Product 3 [3 Blu-ray]</Title>
                </SimilarProduct>
                <SimilarProduct>
                    <ASIN>X100Y200W4</ASIN>
                    <Title>Similar Product 4 [Blu-ray]</Title>
                </SimilarProduct>
            </SimilarProducts>
            <BrowseNodes>
                <BrowseNode>
                    <BrowseNodeId>000000000</BrowseNodeId>
                    <Name>Sample Title</Name>
                    <Ancestors>
                        <BrowseNode>
                            <BrowseNodeId>00000001</BrowseNodeId>
                            <Name>B</Name>
                            <Ancestors>
                                <BrowseNode>
                                    <BrowseNodeId>00000002</BrowseNodeId>
                                    <Name>Serien A - Z</Name>
                                    <Ancestors>
                                        <BrowseNode>
                                            <BrowseNodeId>000001</BrowseNodeId>
                                            <Name>TV-Serien &amp; TV-Produktionen</Name>
                                            <Ancestors>
                                                <BrowseNode>
                                                    <BrowseNodeId>000002</BrowseNodeId>
                                                    <Name>Genres</Name>
                                                    <IsCategoryRoot>1</IsCategoryRoot>
                                                    <Ancestors>
                                                        <BrowseNode>
                                                            <BrowseNodeId>000003</BrowseNodeId>
                                                            <Name>DVD &amp; Blu-ray</Name>
                                                        </BrowseNode>
                                                    </Ancestors>
                                                </BrowseNode>
                                            </Ancestors>
                                        </BrowseNode>
                                    </Ancestors>
                                </BrowseNode>
                            </Ancestors>
                        </BrowseNode>
                    </Ancestors>
                </BrowseNode>
                <BrowseNode>
                    <BrowseNodeId>00000002</BrowseNodeId>
                    <Name>Drama</Name>
                    <Ancestors>
                        <BrowseNode>
                            <BrowseNodeId>000001</BrowseNodeId>
                            <Name>TV-Serien &amp; TV-Produktionen</Name>
                            <Ancestors>
                                <BrowseNode>
                                    <BrowseNodeId>000002</BrowseNodeId>
                                    <Name>Genres</Name>
                                    <IsCategoryRoot>1</IsCategoryRoot>
                                    <Ancestors>
                                        <BrowseNode>
                                            <BrowseNodeId>000003</BrowseNodeId>
                                            <Name>DVD &amp; Blu-ray</Name>
                                        </BrowseNode>
                                    </Ancestors>
                                </BrowseNode>
                            </Ancestors>
                        </BrowseNode>
                    </Ancestors>
                </BrowseNode>
            </BrowseNodes>
        </Item>
    """

    def test_set_failed_to_sync(self):
        asin = 'ASINASINASIN'
        p = Product.objects.create(asin=asin)
        self.assertIsNotNone(p)
        self.assertEqual(asin, p.asin)
        self.assertEqual(0, p.status)

        p.set_failed_to_sync()
        self.assertEqual(2, p.status)

    def __get_sample_amazon_product(self):
        return AmazonProduct(objectify.fromstring(self.test_xml), None, None, None)


if __name__ == '__main__':
    unittest.main()
