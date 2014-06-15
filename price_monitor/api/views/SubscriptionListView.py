from price_monitor.api.serializers.SubscriptionSerializer import SubscriptionSerializer
from price_monitor.models.Subscription import Subscription

from rest_framework import generics, permissions


class SubscriptionListView(generics.ListAPIView):
    """
    Returns list of subscriptions, if user is authenticated
    """
    model = Subscription
    serializer_class = SubscriptionSerializer
    permission_classes = [
        # only return the list if user is authenticated
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        """
        Filters queryset by the authenticated user
        :returns: filtered EmailNotification objects
        :rtype:   QuerySet
        """
        return super(SubscriptionListView, self).get_queryset().filter(owner=self.request.user)
