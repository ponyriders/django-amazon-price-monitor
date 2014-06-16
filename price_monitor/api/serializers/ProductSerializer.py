from price_monitor.models import Product

from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    """
    Product serializer. Serializes all fields needed for frontend and id from asin.
    Also sets all fields but asin to read only
    """
    id = serializers.CharField(source='asin')

    class Meta:
        model = Product
        fields = (
            'id',
            'date_creation',
            'date_updated',
            'date_last_synced',
            'status',

            # amazon specific fields
            'asin',
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
