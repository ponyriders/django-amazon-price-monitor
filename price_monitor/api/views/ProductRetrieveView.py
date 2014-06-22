from price_monitor.api.serializers.ProductSerializer import ProductSerializer
from price_monitor.models.Product import Product

from rest_framework import generics, permissions


class ProductRetrieveView(generics.RetrieveAPIView):
    """
    Returns list of Products, if user is authenticated
    """
    model = Product
    serializer_class = ProductSerializer
    lookup_field = 'asin'
    permission_classes = [
        # only return the list if user is authenticated
        permissions.IsAuthenticated
    ]
