from price_monitor.api.serializers.ProductSerializer import ProductSerializer
from price_monitor.models import Subscription

from rest_framework import serializers


class SubscriptionSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Subscription
        fields = (
            'public_id',
            'price_limit',
            'product',
            'date_last_notification',
            'email_notification',
        )
