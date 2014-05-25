from djangular.views.crud import NgCRUDView

from ...models.Product import Product


class ProductCRUDView(NgCRUDView):
    """
    View handling CRUD methods on an product.
    """
    model = Product

    def get_queryset(self):
        """
        Filters queryset to empty queryset if user is not authenticated
        :return:    Filtered products
        :rtype:     QuerySet
        """
        if not self.request.user.is_authenticated():
            return self.model.objects.none()
        return super(ProductCRUDView, self).get_queryset()
