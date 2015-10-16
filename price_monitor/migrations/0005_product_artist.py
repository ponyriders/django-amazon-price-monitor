# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('price_monitor', '0004_make_price_and_currency_nullable'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='artist',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Artist'),
        ),
    ]
