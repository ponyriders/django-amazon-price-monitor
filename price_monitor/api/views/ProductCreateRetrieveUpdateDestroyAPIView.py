from .mixins.ProductFilteringMixin import ProductFilteringMixin
from ..serializers.ProductSerializer import ProductSerializer
from ...models.Product import Product

from rest_framework import generics, mixins, permissions


class ProductCreateRetrieveUpdateDestroyAPIView(ProductFilteringMixin, mixins.CreateModelMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Returns single instance of Product, if user is authenticated
    """
    model = Product
    serializer_class = ProductSerializer
    lookup_field = 'asin'
    permission_classes = [
        # only return the product if user is authenticated
        permissions.IsAuthenticated
    ]

    def post(self, request, *args, **kwargs):
        """
        Add post method to create object
        :param request: the request
        :type request:  HttpRequest
        :return:        Result of creation
        :rtype:         HttpResponse
        """
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        """
        Filters queryset by the authenticated user
        :returns: filtered Product objects
        :rtype:   QuerySet
        """
        # distinct is needed to prevent multiple instances of product in resultset if multiple subscriptions are present
        return self.model.objects.filter(subscription__owner=self.request.user).distinct()

    def perform_destroy(self, instance):
        """
        Overwrite base function to delete subscriptions, not the product itself
        :param instance: the product to delete subscriptions from
        :type instance:  Product
        """
        instance.subscription_set.filter(owner=self.request.user).delete()
