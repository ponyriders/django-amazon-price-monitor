from price_monitor.api.serializers.ProductSerializer import ProductSerializer
from price_monitor.models.Product import Product

from rest_framework import generics, permissions


class ProductListView(generics.ListAPIView):
    model = Product
    serializer_class = ProductSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
