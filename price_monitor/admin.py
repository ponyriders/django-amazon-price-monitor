from django.contrib import admin

from price_monitor.models import (
    Price,
    Product,
)


class PriceAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(Price, PriceAdmin)
admin.site.register(Product, PriceAdmin)

