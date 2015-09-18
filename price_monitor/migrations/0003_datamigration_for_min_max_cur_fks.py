# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def set_prices(apps, schema_editor):
    """
    Sets min, max and current price
    """
    for product in apps.get_model('price_monitor', 'Product').objects.all():
        if product.price_set.count() > 0:
            product.current_price = product.price_set.latest('date_seen')
            product.highest_price = product.price_set.latest('value')
            product.lowest_price = product.price_set.earliest('value')
            product.save()


class Migration(migrations.Migration):

    dependencies = [
        ('price_monitor', '0002_add_min_max_fk_to_product'),
    ]

    operations = [
        migrations.RunPython(set_prices, reverse_code=migrations.RunPython.noop),
    ]
