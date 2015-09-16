from rest_framework import generics, permissions

from .mixins.ProductFilteringMixin import ProductFilteringMixin
from ..serializers.ProductSerializer import ProductSerializer
from ...models.Product import Product


class ProductListView(ProductFilteringMixin, generics.ListAPIView):
    """
    Returns list of Products and provides endpoint to create Products,
    if user is authenticated
    """
    model = Product
    serializer_class = ProductSerializer
    allow_empty = True
    queryset = Product.objects.all()
    permission_classes = [
        # only return the list if user is authenticated
        permissions.IsAuthenticated
    ]
