from djangular.views.crud import NgCRUDView

from ...models.Subscription import Subscription


class SubscriptionCRUDView(NgCRUDView):
    """
    View handling CRUD methods on an product.
    """
    model = Subscription

    def get_queryset(self):
        """
        Filters queryset to empty queryset if user is not authenticated and by owner if user is authenticated
        :return:    Filtered subscriptions
        :rtype:     QuerySet
        """
        if not self.request.user.is_authenticated():
            return self.model.objects.none()
        return super(SubscriptionCRUDView, self).get_queryset().filter(owner=self.request.user)
