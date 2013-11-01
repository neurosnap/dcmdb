# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Series.series_number'
        db.alter_column(u'dcmupload_series', 'series_number', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Image.image_number'
        db.alter_column(u'dcmupload_image', 'image_number', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'Series.series_number'
        db.alter_column(u'dcmupload_series', 'series_number', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Image.image_number'
        db.alter_column(u'dcmupload_image', 'image_number', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'dcm_study': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dcmupload.Study']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'laterality': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'modality': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'series_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'dcmupload.study': {
            'Meta': {'object_name': 'Study'},
            'UID': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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