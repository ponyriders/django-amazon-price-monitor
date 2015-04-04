from ..serializers.SubscriptionSerializer import SubscriptionSerializer
from ...models.Subscription import Subscription

from rest_framework import generics, permissions


class SubscriptionListView(generics.ListAPIView):
    """
    Returns list of subscriptions, if user is authenticated
    """
    model = Subscription
    serializer_class = SubscriptionSerializer
    allow_empty = True

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
        return self.model.objects.filter(owner=self.request.user)
