# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('price_monitor', '0003_datamigration_for_min_max_cur_fks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='currency',
            field=models.CharField(null=True, verbose_name='Currency', blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='price',
            name='value',
            field=models.FloatField(null=True, verbose_name='Price', blank=True),
        ),
    ]
