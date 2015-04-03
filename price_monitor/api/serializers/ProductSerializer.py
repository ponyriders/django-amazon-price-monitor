from .SubscriptionSerializer import SubscriptionSerializer
from ...models import EmailNotification, Product

from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    """
    Product serializer. Serializes all fields needed for frontend and id from asin.
    Also sets all fields but asin to read only
    """

    asin = serializers.CharField(max_length=100)
    current_price = serializers.SerializerMethodField('get_price_values')
    subscription_set = SubscriptionSerializer(many=True)

    def get_price_values(self, obj):
        """
        Renderes price dict as read only value into product representation
        :param obj: product to get price for
        :type obj:  Product
        :returns:   Dict with price values
        :rtype:     dict
        """
        try:
            price = obj.price_set.order_by('-date_seen')[0]
        except IndexError:
            return None
        else:
            return {
                'value': price.value,
                'currency': price.currency,
                'date_seen': price.date_seen,
            }

    def create(self, validated_data):
        """
        Overwriting default create function to ensure, that the already
        existing instance of product is used, if asin is already in database
        :param validated_data: valid form data
        :type validated_data:  dict
        :return:               created or fetched product
        :rtype:                Product
        """
        product = Product.objects.get_or_create(asin=validated_data['asin'])[0]

        for new_subscription in validated_data['subscription_set']:
            # first fetch EmailNotification object
            email_notification = EmailNotification.objects.get_or_create(
                owner=self.context['request'].user,
                email=new_subscription['email_notification']['email']
            )[0]

            # don't create double subscriptions with same price limit
            product.subscription_set.get_or_create(
                owner=self.context['request'].user,
                price_limit=new_subscription['price_limit'],
                email_notification=email_notification
            )
        return product

    class Meta:
        model = Product
        fields = (
            'date_creation',
            'date_updated',
            'date_last_synced',
            'status',

            # amazon specific fields
            'asin',
            'title',
            'isbn',
            'eisbn',
            'binding',
            'date_publication',
            'date_release',

            # amazon urls
            'large_image_url',
            'medium_image_url',
            'small_image_url',
            'offer_url',
            'current_price',
            'subscription_set',
        )
        # TODO: check if this is good
        read_only_fields = (
            'date_creation',
            'date_updated',
            'date_last_synced',
            'status',

            # amazon specific fields
            'title',
            'isbn',
            'eisbn',
            'author',
            'publisher',
            'label',
            'manufacturer',
            'brand',
            'binding',
            'pages',
            'date_publication',
            'date_release',
            'edition',
            'model',
            'part_number',

            # amazon urls
            'large_image_url',
            'medium_image_url',
            'small_image_url',
            'tiny_image_url',
            'offer_url',
        )
