# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Product'
        db.create_table('prescriptions_product', (
            ('bnf_code', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, blank=True)),
        ))
        db.send_create_signal('prescriptions', ['Product'])

        # Adding model 'Prescription'
        db.create_table('prescriptions_prescription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prescriptions.Product'])),
            ('practice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['practices.Practice'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('nic', self.gf('django.db.models.fields.FloatField')()),
            ('actual_cost', self.gf('django.db.models.fields.FloatField')()),
            ('period', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
        ))
        db.send_create_signal('prescriptions', ['Prescription'])


    def backwards(self, orm):
        # Deleting model 'Product'
        db.delete_table('prescriptions_product')

        # Deleting model 'Prescription'
        db.delete_table('prescriptions_prescription')


    models = {
        'practices.practice': {
            'Meta': {'object_name': 'Practice'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'geography': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'practice': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'})
        },
        'prescriptions.prescription': {
            'Meta': {'object_name': 'Prescription'},
            'actual_cost': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nic': ('django.db.models.fields.FloatField', [], {}),
            'period': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'practice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['practices.Practice']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prescriptions.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'prescriptions.product': {
            'Meta': {'object_name': 'Product'},
            'bnf_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['prescriptions']