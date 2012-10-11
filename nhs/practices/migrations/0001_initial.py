# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Practice'
        db.create_table('practices_practice', (
            ('practice', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, geography=True)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('practices', ['Practice'])


    def backwards(self, orm):
        # Deleting model 'Practice'
        db.delete_table('practices_practice')


    models = {
        'practices.practice': {
            'Meta': {'object_name': 'Practice'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'geography': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'practice': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'})
        }
    }

    complete_apps = ['practices']