from .EmailNotificationSerializer import EmailNotificationSerializer
from ...models import Subscription

from rest_framework import serializers


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializes subscription with product inline. Also renders id frm public_id
    """
    # this field needs to be writable to get it's value into update function of ProductSerializer
    id = serializers.CharField(source='public_id', required=False)
    email_notification = EmailNotificationSerializer()

    class Meta:
        model = Subscription
        fields = (
            'id',
            'price_limit',
            'date_last_notification',
            'email_notification',
        )

        read_only_fields = (
            'date_last_notification',
        )
