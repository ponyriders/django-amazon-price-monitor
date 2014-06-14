from price_monitor.models import Subscription

from rest_framework import serializers


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = (
            'public_id',
            'product',
            'price_limit',
            'date_last_notification',
            'email_notification',
        )
