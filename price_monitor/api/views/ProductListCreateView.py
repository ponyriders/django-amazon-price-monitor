from ..serializers.ProductSerializer import ProductSerializer
from ...models.Product import Product

from rest_framework import generics, permissions


class ProductListCreateView(generics.ListCreateAPIView):
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
        return self.model.objects.filter(subscription__owner=self.request.user)
