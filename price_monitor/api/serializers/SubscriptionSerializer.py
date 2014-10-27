from .EmailNotificationSerializer import EmailNotificationSerializer
from ...models import Subscription

from rest_framework import serializers


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializes subscription with product inline. Also renders id frm public_id
    """
    id = serializers.CharField(source='public_id')
    email_notification = EmailNotificationSerializer()

    class Meta:
        model = Subscription
        fields = (
            'id',
            'price_limit',
            'product',
            'date_last_notification',
            'email_notification',
        )
