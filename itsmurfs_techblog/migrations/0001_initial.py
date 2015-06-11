# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Smurf'
        db.create_table(u'itsmurfs_techblog_smurf', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('job_title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('workplace', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('workarea', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('profile_image', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('presentation_post', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('num_post', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'itsmurfs_techblog', ['Smurf'])

        # Adding model 'Mention'
        db.create_table(u'itsmurfs_techblog_mention', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('genera_description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('smurf', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mentions', to=orm['itsmurfs_techblog.Smurf'])),
        ))
        db.send_create_signal(u'itsmurfs_techblog', ['Mention'])

        # Adding model 'ReferenceSite'
        db.create_table(u'itsmurfs_techblog_referencesite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('smurf', self.gf('django.db.models.fields.related.ForeignKey')(related_name='references', to=orm['itsmurfs_techblog.Smurf'])),
        ))
        db.send_create_signal(u'itsmurfs_techblog', ['ReferenceSite'])


    def backwards(self, orm):
        # Deleting model 'Smurf'
        db.delete_table(u'itsmurfs_techblog_smurf')

        # Deleting model 'Mention'
        db.delete_table(u'itsmurfs_techblog_mention')

        # Deleting model 'ReferenceSite'
        db.delete_table(u'itsmurfs_techblog_referencesite')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'codename',)", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'itsmurfs_techblog.mention': {
            'Meta': {'object_name': 'Mention'},
            'genera_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'smurf': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mentions'", 'to': u"orm['itsmurfs_techblog.Smurf']"})
        },
        u'itsmurfs_techblog.referencesite': {
            'Meta': {'object_name': 'ReferenceSite'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'smurf': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'references'", 'to': u"orm['itsmurfs_techblog.Smurf']"})
        },
        u'itsmurfs_techblog.smurf': {
            'Meta': {'object_name': 'Smurf'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'num_post': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'presentation_post': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'profile_image': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'workarea': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'workplace': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['itsmurfs_techblog']