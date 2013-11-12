# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Series.UID'
        db.alter_column(u'dcmupload_series', 'UID', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'Series.modality'
        db.alter_column(u'dcmupload_series', 'modality', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Series.laterality'
        db.alter_column(u'dcmupload_series', 'laterality', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Series.institution_name'
        db.alter_column(u'dcmupload_series', 'institution_name', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Series.body_part_examined'
        db.alter_column(u'dcmupload_series', 'body_part_examined', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Series.date'
        db.alter_column(u'dcmupload_series', 'date', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Series.manufacturer'
        db.alter_column(u'dcmupload_series', 'manufacturer', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Image.content_time'
        db.alter_column(u'dcmupload_image', 'content_time', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Image.image_position_patient'
        db.alter_column(u'dcmupload_image', 'image_position_patient', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Image.filename'
        db.alter_column(u'dcmupload_image', 'filename', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'Image.content_date'
        db.alter_column(u'dcmupload_image', 'content_date', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Image.image_orientation_patient'
        db.alter_column(u'dcmupload_image', 'image_orientation_patient', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Image.transfer_syntax_uid'
        db.alter_column(u'dcmupload_image', 'transfer_syntax_uid', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Image.patient_position'
        db.alter_column(u'dcmupload_image', 'patient_position', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Image.UID'
        db.alter_column(u'dcmupload_image', 'UID', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'Study.UID'
        db.alter_column(u'dcmupload_study', 'UID', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'Study.sop_class_uid'
        db.alter_column(u'dcmupload_study', 'sop_class_uid', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'Study.accession_number'
        db.alter_column(u'dcmupload_study', 'accession_number', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Study.study_time'
        db.alter_column(u'dcmupload_study', 'study_time', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Study.study_id'
        db.alter_column(u'dcmupload_study', 'study_id', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Study.study_date'
        db.alter_column(u'dcmupload_study', 'study_date', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Study.description'
        db.alter_column(u'dcmupload_study', 'description', self.gf('django.db.models.fields.CharField')(max_length=2500, null=True))

    def backwards(self, orm):

        # Changing field 'Series.UID'
        db.alter_column(u'dcmupload_series', 'UID', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Series.modality'
        db.alter_column(u'dcmupload_series', 'modality', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Series.laterality'
        db.alter_column(u'dcmupload_series', 'laterality', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Series.institution_name'
        db.alter_column(u'dcmupload_series', 'institution_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Series.body_part_examined'
        db.alter_column(u'dcmupload_series', 'body_part_examined', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Series.date'
        db.alter_column(u'dcmupload_series', 'date', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Series.manufacturer'
        db.alter_column(u'dcmupload_series', 'manufacturer', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Image.content_time'
        db.alter_column(u'dcmupload_image', 'content_time', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Image.image_position_patient'
        db.alter_column(u'dcmupload_image', 'image_position_patient', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Image.filename'
        db.alter_column(u'dcmupload_image', 'filename', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Image.content_date'
        db.alter_column(u'dcmupload_image', 'content_date', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Image.image_orientation_patient'
        db.alter_column(u'dcmupload_image', 'image_orientation_patient', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Image.transfer_syntax_uid'
        db.alter_column(u'dcmupload_image', 'transfer_syntax_uid', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Image.patient_position'
        db.alter_column(u'dcmupload_image', 'patient_position', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Image.UID'
        db.alter_column(u'dcmupload_image', 'UID', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Study.UID'
        db.alter_column(u'dcmupload_study', 'UID', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True))

        # Changing field 'Study.sop_class_uid'
        db.alter_column(u'dcmupload_study', 'sop_class_uid', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Study.accession_number'
        db.alter_column(u'dcmupload_study', 'accession_number', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Study.study_time'
        db.alter_column(u'dcmupload_study', 'study_time', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Study.study_id'
        db.alter_column(u'dcmupload_study', 'study_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Study.study_date'
        db.alter_column(u'dcmupload_study', 'study_date', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Study.description'
        db.alter_column(u'dcmupload_study', 'description', self.gf('django.db.models.fields.CharField')(max_length=500, null=True))

    models = {
        u'dcmupload.image': {
            'Meta': {'object_name': 'Image'},
            'UID': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'content_date': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'content_time': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dcm_series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dcmupload.Series']"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_gen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'image_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'image_orientation_patient': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'image_position_patient': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'patient_position': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'transfer_syntax_uid': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'dcmupload.series': {
            'Meta': {'object_name': 'Series'},
            'UID': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'body_part_examined': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'dcm_study': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dcmupload.Study']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'laterality': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'modality': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'series_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'series_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'dcmupload.study': {
            'Meta': {'object_name': 'Study'},
            'UID': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'accession_number': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sop_class_uid': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'study_date': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'study_id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'study_time': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['dcmupload']