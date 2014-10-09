# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Product.manufacturer'
        db.delete_column('price_monitor_product', 'manufacturer')

        # Deleting field 'Product.publisher'
        db.delete_column('price_monitor_product', 'publisher')

        # Deleting field 'Product.author'
        db.delete_column('price_monitor_product', 'author')

        # Deleting field 'Product.edition'
        db.delete_column('price_monitor_product', 'edition')

        # Deleting field 'Product.model'
        db.delete_column('price_monitor_product', 'model')

        # Deleting field 'Product.label'
        db.delete_column('price_monitor_product', 'label')

        # Deleting field 'Product.brand'
        db.delete_column('price_monitor_product', 'brand')

        # Deleting field 'Product.part_number'
        db.delete_column('price_monitor_product', 'part_number')

        # Deleting field 'Product.pages'
        db.delete_column('price_monitor_product', 'pages')

        # Adding field 'Product.audience_rating'
        db.add_column('price_monitor_product', 'audience_rating',
                      self.gf('django.db.models.fields.CharField')(blank=True, null=True, max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Product.manufacturer'
        db.add_column('price_monitor_product', 'manufacturer',
                      self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=255),
                      keep_default=False)

        # Adding field 'Product.publisher'
        db.add_column('price_monitor_product', 'publisher',
                      self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=255),
                      keep_default=False)

        # Adding field 'Product.author'
        db.add_column('price_monitor_product', 'author',
                      self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=255),
                      keep_default=False)

        # Adding field 'Product.edition'
        db.add_column('price_monitor_product', 'edition',
                      self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=255),
                      keep_default=False)

        # Adding field 'Product.model'
        db.add_column('price_monitor_product', 'model',
                      self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=255),
                      keep_default=False)

        # Adding field 'Product.label'
        db.add_column('price_monitor_product', 'label',
                      self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=255),
                      keep_default=False)

        # Adding field 'Product.brand'
        db.add_column('price_monitor_product', 'brand',
                      self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=255),
                      keep_default=False)

        # Adding field 'Product.part_number'
        db.add_column('price_monitor_product', 'part_number',
                      self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=255),
                      keep_default=False)

        # Adding field 'Product.pages'
        db.add_column('price_monitor_product', 'pages',
                      self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Product.audience_rating'
        db.delete_column('price_monitor_product', 'audience_rating')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'price_monitor.emailnotification': {
            'Meta': {'object_name': 'EmailNotification', 'ordering': "('email',)"},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'public_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '36'})
        },
        'price_monitor.price': {
            'Meta': {'object_name': 'Price', 'ordering': "('date_seen',)"},
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'date_seen': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['price_monitor.Product']"}),
            'public_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '36'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'price_monitor.product': {
            'Meta': {'object_name': 'Product', 'ordering': "('title', 'asin')"},
            'asin': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'audience_rating': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '255'}),
            'binding': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '255'}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_synced': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'date_publication': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'date_release': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'eisbn': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '13'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '10'}),
            'large_image_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'medium_image_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'offer_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'small_image_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'through': "orm['price_monitor.Subscription']", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'tiny_image_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '255'})
        },
        'price_monitor.subscription': {
            'Meta': {'object_name': 'Subscription', 'ordering': "('email_notification__email', 'product__title')"},
            'date_last_notification': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'email_notification': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['price_monitor.EmailNotification']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'price_limit': ('django.db.models.fields.FloatField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['price_monitor.Product']"}),
            'public_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '36'})
        }
    }

    complete_apps = ['price_monitor']