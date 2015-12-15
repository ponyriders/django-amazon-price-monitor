"""Serializer for Price model"""
from ...models import Price

from rest_framework import serializers


class PriceSerializer(serializers.ModelSerializer):

    """Serializes prices by showing currency, value and date seen"""

    class Meta(object):

        """Some model meta"""

        model = Price
        fields = (
            'value',
            'currency',
            'date_seen',
        )
