# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Practice.ccg'
        db.add_column('practices_practice', 'ccg',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ccgs.CCG'], null=True),
                      keep_default=False)


        # Changing field 'Practice.location'
        db.alter_column('practices_practice', 'location', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True))

    def backwards(self, orm):
        # Deleting field 'Practice.ccg'
        db.delete_column('practices_practice', 'ccg_id')


        # Changing field 'Practice.location'
        db.alter_column('practices_practice', 'location', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, geography=True))

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
        },
        'practices.practice': {
            'Meta': {'object_name': 'Practice'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ccg': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ccgs.CCG']", 'null': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'practice': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'})
        }
    }

    complete_apps = ['practices']