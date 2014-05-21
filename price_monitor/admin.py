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
    list_display = ('asin', 'title', 'author', 'status', 'date_updated', 'date_last_synced', )

    actions = ['reset_to_created', ]

    def reset_to_created(self, request, queryset):
        queryset.update(status=0)
    reset_to_created.short_description = ugettext_lazy('Reset to status "Created".')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('product', 'price_limit', 'owner', 'date_last_notification', 'get_email_address', 'public_id',)
    list_filter = ('owner__username', 'price_limit', )


class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ('email', 'owner',)


admin.site.register(Price, PriceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(EmailNotification, EmailNotificationAdmin)
