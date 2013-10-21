# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Study'
        db.create_table(u'dcmupload_study', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('UID', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('study_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('study_date', self.gf('django.db.models.fields.DateField')()),
            ('study_time', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('accession_number', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('sop_class_uid', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'dcmupload', ['Study'])

        # Adding model 'Series'
        db.create_table(u'dcmupload_series', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dcm_study', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dcmupload.Study'])),
            ('UID', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('modality', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('institution_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('series_number', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('laterality', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'dcmupload', ['Series'])

        # Adding model 'Image'
        db.create_table(u'dcmupload_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dcm_series', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dcmupload.Series'])),
            ('UID', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image_gen', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('transfer_syntax_uid', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('image_number', self.gf('django.db.models.fields.IntegerField')()),
            ('image_orientation_patient', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('image_position_patient', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('patient_position', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('content_date', self.gf('django.db.models.fields.DateField')(default=None)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'dcmupload', ['Image'])


    def backwards(self, orm):
        # Deleting model 'Study'
        db.delete_table(u'dcmupload_study')

        # Deleting model 'Series'
        db.delete_table(u'dcmupload_series')

        # Deleting model 'Image'
        db.delete_table(u'dcmupload_image')


    models = {
        u'dcmupload.image': {
            'Meta': {'object_name': 'Image'},
            'UID': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_date': ('django.db.models.fields.DateField', [], {'default': 'None'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dcm_series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dcmupload.Series']"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_gen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'image_number': ('django.db.models.fields.IntegerField', [], {}),
            'image_orientation_patient': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'image_position_patient': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'patient_position': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'transfer_syntax_uid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'dcmupload.series': {
            'Meta': {'object_name': 'Series'},
            'UID': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'dcm_study': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dcmupload.Study']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'laterality': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modality': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'series_number': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'dcmupload.study': {
            'Meta': {'object_name': 'Study'},
            'UID': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'accession_number': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sop_class_uid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'study_date': ('django.db.models.fields.DateField', [], {}),
            'study_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'study_time': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['dcmupload']