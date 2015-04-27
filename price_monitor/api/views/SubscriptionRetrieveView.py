from ..serializers.SubscriptionSerializer import SubscriptionSerializer
from ...models.Subscription import Subscription

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
        return self.model.objects.filter(owner=self.request.user)
