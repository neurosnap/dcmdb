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
            ('UID', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('study_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('study_date', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('study_time', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('accession_number', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
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
            ('series_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modality', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('institution_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('series_number', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('body_part_examined', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('laterality', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
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
            ('transfer_syntax_uid', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('image_number', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('image_orientation_patient', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('image_position_patient', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('patient_position', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('content_date', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('content_time', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
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
            'content_date': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'content_time': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dcm_series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dcmupload.Series']"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_gen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'image_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'image_orientation_patient': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'image_position_patient': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'patient_position': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'transfer_syntax_uid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'dcmupload.series': {
            'Meta': {'object_name': 'Series'},
            'UID': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'body_part_examined': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'dcm_study': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dcmupload.Study']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'laterality': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'modality': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'series_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'series_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'dcmupload.study': {
            'Meta': {'object_name': 'Study'},
            'UID': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'accession_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sop_class_uid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'study_date': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'study_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'study_time': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['dcmupload']