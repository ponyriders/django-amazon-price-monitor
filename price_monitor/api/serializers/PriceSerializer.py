from ...models import Price

from rest_framework import serializers


class PriceSerializer(serializers.ModelSerializer):
    """
    Serializes EmailNotification objects. Just renders public_id as id and the email address
    """

    class Meta:
        model = Price
        fields = (
            'value',
            'currency',
            'date_seen',
        )
