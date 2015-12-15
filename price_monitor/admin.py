"""AdminSite definitions"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy

from price_monitor.models import (
    EmailNotification,
    Price,
    Product,
    Subscription,
)


class PriceAdmin(admin.ModelAdmin):

    """Admin for the model Price"""

    list_display = ('date_seen', 'value', 'currency', )
    list_filter = ('product', )


class ProductAdmin(admin.ModelAdmin):

    """Admin for the model Product"""

    list_display = ('asin', 'title', 'artist', 'status', 'date_updated', 'date_last_synced', )
    list_filter = ('status', )
    search_fields = ('asin', )
    readonly_fields = ('current_price', 'highest_price', 'lowest_price',)

    actions = ['reset_to_created', 'resynchronize', ]

    def reset_to_created(self, request, queryset):  # pylint:disable=unused-argument
        """
        Resets the status of the product back to created.
        :param request: sent request
        :param queryset: queryset containing the products
        """
        queryset.update(status=0)
    reset_to_created.short_description = ugettext_lazy('Reset to status "Created".')

    def resynchronize(self, request, queryset):  # pylint:disable=unused-argument
        """
        Synchronizes the sent products with the product advertising api.
        :param request: sent request
        :param queryset: queryset containing the products
        """
        from price_monitor.product_advertising_api.tasks import SynchronizeProductsTask
        for product in queryset:
            SynchronizeProductsTask.delay([product.asin])
    resynchronize.short_description = ugettext_lazy('Resynchronize with API')


class SubscriptionAdmin(admin.ModelAdmin):

    """Admin for the model Subscription"""

    list_display = ('product', 'price_limit', 'owner', 'date_last_notification', 'get_email_address', 'public_id',)
    list_filter = ('owner__username', 'price_limit', )


class EmailNotificationAdmin(admin.ModelAdmin):

    """Admin for the model EmailNotification"""

    list_display = ('email', 'owner', 'public_id',)


admin.site.register(Price, PriceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(EmailNotification, EmailNotificationAdmin)
