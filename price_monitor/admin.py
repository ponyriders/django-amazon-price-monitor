from django.contrib import admin
from django.utils.translation import ugettext_lazy

from price_monitor.models import (
    EmailNotification,
    Price,
    Product,
    Subscription,
)


class PriceAdmin(admin.ModelAdmin):
    list_display = ('date_seen', 'value', 'currency', )
    list_filter = ('product', )


class ProductAdmin(admin.ModelAdmin):
    list_display = ('asin', 'title', 'status', 'date_updated', 'date_last_synced', )
    list_filter = ('status', )
    search_fields = ('asin', )
    readonly_fields = ('current_price', 'highest_price', 'lowest_price',)

    actions = ['reset_to_created', 'resynchronize', ]

    def reset_to_created(self, request, queryset):
        queryset.update(status=0)
    reset_to_created.short_description = ugettext_lazy('Reset to status "Created".')

    def resynchronize(self, request, queryset):
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
    list_display = ('product', 'price_limit', 'owner', 'date_last_notification', 'get_email_address', 'public_id',)
    list_filter = ('owner__username', 'price_limit', )


class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ('email', 'owner', 'public_id',)


admin.site.register(Price, PriceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(EmailNotification, EmailNotificationAdmin)
