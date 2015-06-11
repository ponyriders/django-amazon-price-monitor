# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('price_monitor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='highest_price',
            field=models.ForeignKey(related_name='product_highest', to='price_monitor.Price', blank=True, verbose_name='Highest price ever', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='lowest_price',
            field=models.ForeignKey(related_name='product_lowest', to='price_monitor.Price', blank=True, verbose_name='Lowest price ever', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='current_price',
            field=models.ForeignKey(to='price_monitor.Price', null=True, blank=True, verbose_name='Current price', related_name='product_current'),
        ),
    ]
