# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailNotification',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('public_id', models.CharField(db_index=True, unique=True, editable=False, verbose_name='Public-ID', max_length=36)),
                ('email', models.EmailField(verbose_name='Email address', max_length=254)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'ordering': ('email',),
                'verbose_name': 'Email Notification',
                'verbose_name_plural': 'Email Notifications',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('value', models.FloatField(verbose_name='Price')),
                ('currency', models.CharField(verbose_name='Currency', max_length=3)),
                ('date_seen', models.DateTimeField(verbose_name='Date of price')),
            ],
            options={
                'ordering': ('date_seen',),
                'get_latest_by': 'date_seen',
                'verbose_name': 'Price',
                'verbose_name_plural': 'Prices',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date_creation', models.DateTimeField(verbose_name='Date of creation', auto_now_add=True)),
                ('date_updated', models.DateTimeField(verbose_name='Date of last update', auto_now=True)),
                ('date_last_synced', models.DateTimeField(null=True, verbose_name='Date of last synchronization', blank=True)),
                ('status', models.SmallIntegerField(verbose_name='Status', choices=[(0, 'Created'), (1, 'Synced over API'), (2, 'Unsynchable')], default=0)),
                ('asin', models.CharField(unique=True, verbose_name='ASIN', max_length=100)),
                ('title', models.CharField(null=True, verbose_name='Title', blank=True, max_length=255)),
                ('isbn', models.CharField(null=True, verbose_name='ISBN', blank=True, max_length=10)),
                ('eisbn', models.CharField(null=True, verbose_name='E-ISBN', blank=True, max_length=13)),
                ('binding', models.CharField(null=True, verbose_name='Binding', blank=True, max_length=255)),
                ('date_publication', models.DateField(null=True, verbose_name='Publication date', blank=True)),
                ('date_release', models.DateField(null=True, verbose_name='Release date', blank=True)),
                ('audience_rating', models.CharField(null=True, verbose_name='Audience rating', blank=True, max_length=255)),
                ('large_image_url', models.URLField(null=True, verbose_name='URL to large product image', blank=True)),
                ('medium_image_url', models.URLField(null=True, verbose_name='URL to medium product image', blank=True)),
                ('small_image_url', models.URLField(null=True, verbose_name='URL to small product image', blank=True)),
                ('offer_url', models.URLField(null=True, verbose_name='URL to the offer', blank=True)),
            ],
            options={
                'ordering': ('title', 'asin'),
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('public_id', models.CharField(db_index=True, unique=True, editable=False, verbose_name='Public-ID', max_length=36)),
                ('price_limit', models.FloatField(verbose_name='Price limit')),
                ('date_last_notification', models.DateTimeField(null=True, verbose_name='Date of last sent notification', blank=True)),
                ('email_notification', models.ForeignKey(to='price_monitor.EmailNotification', verbose_name='Email Notification')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
                ('product', models.ForeignKey(to='price_monitor.Product', verbose_name='Product')),
            ],
            options={
                'ordering': ('product__title', 'price_limit', 'email_notification__email'),
                'verbose_name': 'Subscription',
                'verbose_name_plural': 'Subscriptions',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='subscribers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Subscribers', through='price_monitor.Subscription'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='price',
            name='product',
            field=models.ForeignKey(to='price_monitor.Product', verbose_name='Product'),
            preserve_default=True,
        ),
    ]
