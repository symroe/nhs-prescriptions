# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table('prescriptions_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('prescriptions', ['Group'])

        # Adding M2M table for field drugs on 'Group'
        db.create_table('prescriptions_group_drugs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['prescriptions.group'], null=False)),
            ('product', models.ForeignKey(orm['prescriptions.product'], null=False))
        ))
        db.create_unique('prescriptions_group_drugs', ['group_id', 'product_id'])


    def backwards(self, orm):
        # Deleting model 'Group'
        db.delete_table('prescriptions_group')

        # Removing M2M table for field drugs on 'Group'
        db.delete_table('prescriptions_group_drugs')


    models = {
        'practices.practice': {
            'Meta': {'object_name': 'Practice'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'geography': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'practice': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'})
        },
        'prescriptions.group': {
            'Meta': {'object_name': 'Group'},
            'drugs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['prescriptions.Product']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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