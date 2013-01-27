# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CCG'
        db.create_table('ccgs_ccg', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=False)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('population', self.gf('django.db.models.fields.IntegerField')()),
            ('lsoa_count', self.gf('django.db.models.fields.IntegerField')()),
            ('poly', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal('ccgs', ['CCG'])


    def backwards(self, orm):
        # Deleting model 'CCG'
        db.delete_table('ccgs_ccg')


    models = {
        'ccgs.ccg': {
            'Meta': {'object_name': 'CCG'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lsoa_count': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'poly': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'population': ('django.db.models.fields.IntegerField', [], {}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['ccgs']