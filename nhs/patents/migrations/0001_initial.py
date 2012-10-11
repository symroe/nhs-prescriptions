# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Patent'
        db.create_table('patents_patent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('drug', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prescriptions.Product'])),
            ('expiry_date', self.gf('django.db.models.fields.DateField')()),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('patents', ['Patent'])


    def backwards(self, orm):
        # Deleting model 'Patent'
        db.delete_table('patents_patent')


    models = {
        'patents.patent': {
            'Meta': {'object_name': 'Patent'},
            'drug': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prescriptions.Product']"}),
            'expiry_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'prescriptions.product': {
            'Meta': {'object_name': 'Product'},
            'bnf_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['patents']