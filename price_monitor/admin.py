from django.contrib import admin

from price_monitor.models import (
    Price,
    Product,
)


class PriceAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    list_display = ('asin', 'title', 'status', 'date_updated', )


admin.site.register(Price, PriceAdmin)
admin.site.register(Product, ProductAdmin)

