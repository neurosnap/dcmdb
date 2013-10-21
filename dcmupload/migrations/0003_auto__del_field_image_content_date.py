# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Image.content_date'
        db.delete_column(u'dcmupload_image', 'content_date')


    def backwards(self, orm):
        # Adding field 'Image.content_date'
        db.add_column(u'dcmupload_image', 'content_date',
                      self.gf('django.db.models.fields.DateField')(default=None, auto_now=True, blank=True),
                      keep_default=False)


    models = {
        u'dcmupload.image': {
            'Meta': {'object_name': 'Image'},
            'UID': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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