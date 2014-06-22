from price_monitor.api.serializers.SubscriptionSerializer import SubscriptionSerializer
from price_monitor.models.Subscription import Subscription

from rest_framework import generics, permissions


class SubscriptionRetrieveView(generics.RetrieveAPIView):
    """
    Returns instance of Subscription, if user is authenticated
    """
    model = Subscription
    serializer_class = SubscriptionSerializer
    lookup_field = 'public_id'
    permission_classes = [
        # only return the list if user is authenticated
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        """
        Filters queryset by the authenticated user
        :returns: filtered Subscription objects
        :rtype:   QuerySet
        """
        return super(SubscriptionRetrieveView, self).get_queryset().filter(owner=self.request.user)
