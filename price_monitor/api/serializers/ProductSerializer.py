from .SubscriptionSerializer import SubscriptionSerializer
from ...models import EmailNotification, Product, Subscription

from django.db import transaction

from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    """
    Product serializer. Serializes all fields needed for frontend and id from asin.
    Also sets all fields but asin to read only
    """

    asin = serializers.CharField(max_length=100)

    # for these three values get_{{ value name }} is the default, but DRF prohibits setting the default value ...
    current_price = serializers.SerializerMethodField()
    highest_price = serializers.SerializerMethodField()
    lowest_price = serializers.SerializerMethodField()
    image_urls = serializers.SerializerMethodField()
    subscription_set = SubscriptionSerializer(many=True)

    def __render_price_dict(self, price):
        """
        Renders price instance as dict
        :param price: price instance
        :type price:  Price
        :return:      price instance as dict
        :rtype:       dict
        """
        return {
            'value': price.value,
            'currency': price.currency,
            'date_seen': price.date_seen,
        }

    def get_current_price(self, obj):
        """
        Renderes current price dict as read only value into product representation
        :param obj: product to get price for
        :type obj:  Product
        :returns:   Dict with current price values
        :rtype:     dict
        """
        if obj.current_price:
            return self.__render_price_dict(obj.current_price)

    def get_highest_price(self, obj):
        """
        Renders highest price dict as read only value into product representation
        :param obj: product to get price for
        :type obj:  Product
        :returns:   Dict with highest price values
        :rtype:     dict
        """
        if obj.highest_price:
            return self.__render_price_dict(obj.highest_price)

    def get_lowest_price(self, obj):
        """
        Renders lowest price dict as read only value into product representation
        :param obj: product to get price for
        :type obj:  Product
        :returns:   Dict with lowest price values
        :rtype:     dict
        """
        if obj.lowest_price:
            return self.__render_price_dict(obj.lowest_price)

    def get_image_urls(self, obj):
        """
        Renders image urls as read only value into product representation
        :param obj: object to get image urls for
        :type obj:  Product
        :returns:   dict with image urls
        :rtype:     dict
        """
        return obj.get_image_urls()

    @transaction.atomic
    def create(self, validated_data):
        """
        Overwriting default create function to ensure, that the already
        existing instance of product is used, if asin is already in database
        :param validated_data: valid form data
        :type validated_data:  dict
        :return:               created or fetched product
        :rtype:                Product
        """
        # product = Product.objects.get_or_create(asin=validated_data['asin'])[0]
        try:
            product = Product.objects.get(asin__iexact=validated_data['asin'])
        except Product.DoesNotExist:
            product = Product.objects.create(asin=validated_data['asin'])

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

    def update(self, instance, validated_data):
        """
        Overwrites parent function to enable update of products subscriptions
        :param instance:        the product instance
        :type instance:         Product
        :param validated_data:  dict with validated data from request
        :type validated_data:   dict
        :returns:               Updated product instance (in fact there are only updates to subscriptions)
        :rtype:                 Product
        """
        new_public_ids = []
        for value_dict in validated_data['subscription_set']:
            # get public_id if there is any
            public_id = value_dict.get('public_id')
            new_public_ids.append(public_id)
            if public_id:
                subscription = Subscription.objects.get_or_create(public_id=public_id)[0]
            else:
                # this is a new line!
                subscription = Subscription()
                subscription.product = instance
                subscription.owner = self.context['request'].user

            subscription.price_limit = value_dict['price_limit']
            # simply create email notifcation object if this is a new address
            subscription.email_notification = EmailNotification.objects.get_or_create(
                owner=self.context['request'].user,
                email=value_dict['email_notification']['email']
            )[0]
            subscription.save()

        # remove all subscriptions not in new set subscriptions
        instance.subscription_set.filter(owner=self.context['request'].user).exclude(public_id__in=new_public_ids).delete()
        return self.context['view'].filter_queryset(self.context['view'].get_queryset()).get(pk=instance.pk)

    class Meta:
        model = Product
        fields = (
            'date_creation',
            'date_updated',
            'date_last_synced',
            'status',
            'subscription_set',

            # amazon specific fields
            'asin',
            'title',
            'isbn',
            'eisbn',
            'binding',
            'date_publication',
            'date_release',

            # amazon urls
            'image_urls',
            'offer_url',
            'current_price',
            'highest_price',
            'lowest_price',
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
            'image_urls',
            'offer_url',
        )
