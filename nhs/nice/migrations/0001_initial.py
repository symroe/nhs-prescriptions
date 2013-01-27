# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Recommendation'
        db.create_table('nice_recommendation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('drug', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prescriptions.Product'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('guideline', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('nice', ['Recommendation'])


    def backwards(self, orm):
        # Deleting model 'Recommendation'
        db.delete_table('nice_recommendation')


    models = {
        'nice.recommendation': {
            'Meta': {'object_name': 'Recommendation'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'drug': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prescriptions.Product']"}),
            'guideline': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'prescriptions.product': {
            'Meta': {'object_name': 'Product'},
            'bnf_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['nice']