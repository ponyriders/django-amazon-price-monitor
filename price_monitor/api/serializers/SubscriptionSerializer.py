from price_monitor.api.serializers.ProductSerializer import ProductSerializer
from price_monitor.models import Subscription

from rest_framework import serializers


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializes subscription with product inline. Also renders id frm public_id
    """
    product = ProductSerializer()
    id = serializers.CharField(source='public_id')

    class Meta:
        model = Subscription
        fields = (
            'id',
            'price_limit',
            'product',
            'date_last_notification',
            'email_notification',
        )
