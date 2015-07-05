from ..serializers.ProductSerializer import ProductSerializer
from ...models.Product import Product

from rest_framework import generics, permissions


class ProductListView(generics.ListAPIView):
    """
    Returns list of Products and provides endpoint to create Products,
    if user is authenticated
    """
    model = Product
    serializer_class = ProductSerializer
    allow_empty = True
    permission_classes = [
        # only return the list if user is authenticated
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        """
        Filters queryset by the authenticated user
        :returns: filtered Product objects
        :rtype:   QuerySet
        """
        # distinct is needed to prevent multiple instances of product in resultset if multiple subscriptions are present
        return self.model.objects\
            .select_related('highest_price', 'lowest_price', 'current_price')\
            .prefetch_related('subscription_set__email_notification')\
            .filter(subscription__owner=self.request.user).distinct()
