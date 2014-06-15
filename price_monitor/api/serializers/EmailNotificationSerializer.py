from price_monitor.models import EmailNotification

from rest_framework import serializers


class EmailNotificationSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='public_id')

    class Meta:
        model = EmailNotification
        fields = (
            'id',
            'email',
        )
