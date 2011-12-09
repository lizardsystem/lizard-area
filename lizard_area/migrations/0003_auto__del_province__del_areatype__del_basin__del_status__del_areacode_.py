# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Province'
        db.delete_table('lizard_area_province')

        # Deleting model 'AreaType'
        db.delete_table('lizard_area_areatype')

        # Deleting model 'Basin'
        db.delete_table('lizard_area_basin')

        # Deleting model 'Status'
        db.delete_table('lizard_area_status')

        # Deleting model 'AreaCode'
        db.delete_table('lizard_area_areacode')

        # Deleting model 'Municipality'
        db.delete_table('lizard_area_municipality')

        # Deleting model 'WaterManagementArea'
        db.delete_table('lizard_area_watermanagementarea')

        # Deleting field 'Communique.code'
        db.delete_column('lizard_area_communique', 'code_id')

        # Deleting field 'Communique.province'
        db.delete_column('lizard_area_communique', 'province_id')

        # Deleting field 'Communique.status'
        db.delete_column('lizard_area_communique', 'status_id')

        # Deleting field 'Communique.watermanagementarea'
        db.delete_column('lizard_area_communique', 'watermanagementarea_id')

        # Deleting field 'Communique.municipality'
        db.delete_column('lizard_area_communique', 'municipality_id')

        # Deleting field 'Communique.basin'
        db.delete_column('lizard_area_communique', 'basin_id')

        # Deleting field 'Communique.area_type'
        db.delete_column('lizard_area_communique', 'area_type_id')

        # Adding field 'Communique.communique'
        db.add_column('lizard_area_communique', 'communique', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'Province'
        db.create_table('lizard_area_province', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, unique=True)),
        ))
        db.send_create_signal('lizard_area', ['Province'])

        # Adding model 'AreaType'
        db.create_table('lizard_area_areatype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, unique=True)),
        ))
        db.send_create_signal('lizard_area', ['AreaType'])

        # Adding model 'Basin'
        db.create_table('lizard_area_basin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, unique=True)),
        ))
        db.send_create_signal('lizard_area', ['Basin'])

        # Adding model 'Status'
        db.create_table('lizard_area_status', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, unique=True)),
        ))
        db.send_create_signal('lizard_area', ['Status'])

        # Adding model 'AreaCode'
        db.create_table('lizard_area_areacode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, unique=True)),
        ))
        db.send_create_signal('lizard_area', ['AreaCode'])

        # Adding model 'Municipality'
        db.create_table('lizard_area_municipality', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, unique=True)),
        ))
        db.send_create_signal('lizard_area', ['Municipality'])

        # Adding model 'WaterManagementArea'
        db.create_table('lizard_area_watermanagementarea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, unique=True)),
        ))
        db.send_create_signal('lizard_area', ['WaterManagementArea'])

        # Adding field 'Communique.code'
        db.add_column('lizard_area_communique', 'code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.AreaCode'], null=True, blank=True), keep_default=False)

        # Adding field 'Communique.province'
        db.add_column('lizard_area_communique', 'province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.Province'], null=True, blank=True), keep_default=False)

        # Adding field 'Communique.status'
        db.add_column('lizard_area_communique', 'status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.Status'], null=True, blank=True), keep_default=False)

        # Adding field 'Communique.watermanagementarea'
        db.add_column('lizard_area_communique', 'watermanagementarea', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.WaterManagementArea'], null=True, blank=True), keep_default=False)

        # Adding field 'Communique.municipality'
        db.add_column('lizard_area_communique', 'municipality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.Municipality'], null=True, blank=True), keep_default=False)

        # Adding field 'Communique.basin'
        db.add_column('lizard_area_communique', 'basin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.Basin'], null=True, blank=True), keep_default=False)

        # Adding field 'Communique.area_type'
        db.add_column('lizard_area_communique', 'area_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.AreaType'], null=True, blank=True), keep_default=False)

        # Deleting field 'Communique.communique'
        db.delete_column('lizard_area_communique', 'communique')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'lizard_area.area': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Area', '_ormbases': ['lizard_area.Communique']},
            'area_class': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'communique_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lizard_area.Communique']", 'unique': 'True', 'primary_key': 'True'}),
            'data_administrator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.DataAdministrator']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Area']", 'null': 'True', 'blank': 'True'})
        },
        'lizard_area.category': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Category'},
            'geo_object_groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_geo.GeoObjectGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapnik_xml_style_sheet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.MapnikXMLStyleSheet']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Category']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'lizard_area.communique': {
            'Meta': {'object_name': 'Communique', '_ormbases': ['lizard_geo.GeoObject']},
            'communique': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'geoobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lizard_geo.GeoObject']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'lizard_area.dataadministrator': {
            'Meta': {'object_name': 'DataAdministrator'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_area.mapnikxmlstylesheet': {
            'Meta': {'object_name': 'MapnikXMLStyleSheet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'source_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'style': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'})
        },
        'lizard_geo.geoobject': {
            'Meta': {'object_name': 'GeoObject'},
            'geo_object_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_geo.GeoObjectGroup']"}),
            'geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'lizard_geo.geoobjectgroup': {
            'Meta': {'object_name': 'GeoObjectGroup'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'source_log': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['lizard_area']
