from price_monitor.api.serializers.SubscriptionSerializer import SubscriptionSerializer
from price_monitor.models.Subscription import Subscription

from rest_framework import generics, permissions


class SubscriptionListView(generics.ListAPIView):
    model = Subscription
    serializer_class = SubscriptionSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return super(SubscriptionListView, self).get_queryset().filter(owner=self.request.user)
