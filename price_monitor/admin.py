from django.contrib import admin
from django.utils.translation import ugettext_lazy

from price_monitor.models import (
    Price,
    Product,
)


class PriceAdmin(admin.ModelAdmin):
    list_display = ('date_seen', 'value', 'currency', )


class ProductAdmin(admin.ModelAdmin):
    list_display = ('asin', 'title', 'status', 'date_updated', )

    actions = ['reset_to_created',]

    def reset_to_created(self, request, queryset):
        queryset.update(status=0)
    reset_to_created.short_description = ugettext_lazy('Reset to status "Created".')



admin.site.register(Price, PriceAdmin)
admin.site.register(Product, ProductAdmin)

