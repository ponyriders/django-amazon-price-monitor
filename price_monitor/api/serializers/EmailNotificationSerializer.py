from ...models import EmailNotification

from rest_framework import serializers


class EmailNotificationSerializer(serializers.ModelSerializer):
    """
    Serializes EmailNotification objects. Just renders public_id as id and the email address
    """
    id = serializers.CharField(source='public_id')

    class Meta:
        model = EmailNotification
        fields = (
            'id',
            'email',
        )
