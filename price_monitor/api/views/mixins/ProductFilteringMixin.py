from django.db.models.query import Prefetch

from ....models.Subscription import Subscription


class ProductFilteringMixin(object):

    def filter_queryset(self, queryset):
        """
        Filters queryset by the authenticated user
        :returns: filtered Product objects
        :rtype:   QuerySet
        """
        queryset = super(ProductFilteringMixin, self).filter_queryset(queryset)
        return queryset\
            .select_related('highest_price', 'lowest_price', 'current_price')\
            .prefetch_related(
                Prefetch(
                    'subscription_set',
                    queryset=Subscription.objects.filter(
                        owner=self.request.user
                    ).select_related('email_notification').distinct()
                )
            ).filter(subscription__owner=self.request.user).distinct()
