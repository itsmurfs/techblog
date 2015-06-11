# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EntryTagsCrossDb'
        db.create_table(u'crossdb_utils_entrytagscrossdb', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_entry', self.gf('django.db.models.fields.CharField')(unique=True, max_length=126)),
        ))
        db.send_create_signal(u'crossdb_utils', ['EntryTagsCrossDb'])

        # Adding model 'MyTag'
        db.create_table(u'crossdb_utils_mytag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'crossdb_utils', ['MyTag'])


    def backwards(self, orm):
        # Deleting model 'EntryTagsCrossDb'
        db.delete_table(u'crossdb_utils_entrytagscrossdb')

        # Deleting model 'MyTag'
        db.delete_table(u'crossdb_utils_mytag')


    models = {
        u'crossdb_utils.entrytagscrossdb': {
            'Meta': {'object_name': 'EntryTagsCrossDb'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_entry': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '126'})
        },
        u'crossdb_utils.mytag': {
            'Meta': {'object_name': 'MyTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['crossdb_utils']