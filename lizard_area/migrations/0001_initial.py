# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'GeoObjectGroup'
        db.create_table('lizard_area_geoobjectgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('source_log', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('lizard_area', ['GeoObjectGroup'])

        # Adding model 'GeoObject'
        db.create_table('lizard_area_geoobject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ident', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.GeometryField')()),
            ('geo_object_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.GeoObjectGroup'])),
        ))
        db.send_create_signal('lizard_area', ['GeoObject'])

        # Adding model 'MapnikXMLStyleSheet'
        db.create_table('lizard_area_mapnikxmlstylesheet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('style', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('source_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('lizard_area', ['MapnikXMLStyleSheet'])

        # Adding model 'Category'
        db.create_table('lizard_area_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.Category'], null=True, blank=True)),
            ('mapnik_xml_style_sheet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.MapnikXMLStyleSheet'], null=True, blank=True)),
        ))
        db.send_create_signal('lizard_area', ['Category'])

        # Adding M2M table for field geo_object_groups on 'Category'
        db.create_table('lizard_area_category_geo_object_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm['lizard_area.category'], null=False)),
            ('geoobjectgroup', models.ForeignKey(orm['lizard_area.geoobjectgroup'], null=False))
        ))
        db.create_unique('lizard_area_category_geo_object_groups', ['category_id', 'geoobjectgroup_id'])

        # Adding model 'DataAdministrator'
        db.create_table('lizard_area_dataadministrator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal('lizard_area', ['DataAdministrator'])

        # Adding model 'AreaCode'
        db.create_table('lizard_area_areacode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal('lizard_area', ['AreaCode'])

        # Adding model 'Status'
        db.create_table('lizard_area_status', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal('lizard_area', ['Status'])

        # Adding model 'AreaType'
        db.create_table('lizard_area_areatype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal('lizard_area', ['AreaType'])

        # Adding model 'Province'
        db.create_table('lizard_area_province', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal('lizard_area', ['Province'])

        # Adding model 'Municipality'
        db.create_table('lizard_area_municipality', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal('lizard_area', ['Municipality'])

        # Adding model 'Basin'
        db.create_table('lizard_area_basin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal('lizard_area', ['Basin'])

        # Adding model 'WaterManagementArea'
        db.create_table('lizard_area_watermanagementarea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal('lizard_area', ['WaterManagementArea'])

        # Adding model 'Communique'
        db.create_table('lizard_area_communique', (
            ('geoobject_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lizard_area.GeoObject'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.AreaCode'], null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.Status'], null=True, blank=True)),
            ('area_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.AreaType'], null=True, blank=True)),
            ('province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.Province'], null=True, blank=True)),
            ('municipality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.Municipality'], null=True, blank=True)),
            ('basin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.Basin'], null=True, blank=True)),
            ('watermanagementarea', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.WaterManagementArea'], null=True, blank=True)),
        ))
        db.send_create_signal('lizard_area', ['Communique'])

        # Adding model 'Area'
        db.create_table('lizard_area_area', (
            ('communique_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lizard_area.Communique'], unique=True, primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.Area'], null=True, blank=True)),
            ('data_administrator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.DataAdministrator'])),
            ('area_class', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('lizard_area', ['Area'])


    def backwards(self, orm):
        
        # Deleting model 'GeoObjectGroup'
        db.delete_table('lizard_area_geoobjectgroup')

        # Deleting model 'GeoObject'
        db.delete_table('lizard_area_geoobject')

        # Deleting model 'MapnikXMLStyleSheet'
        db.delete_table('lizard_area_mapnikxmlstylesheet')

        # Deleting model 'Category'
        db.delete_table('lizard_area_category')

        # Removing M2M table for field geo_object_groups on 'Category'
        db.delete_table('lizard_area_category_geo_object_groups')

        # Deleting model 'DataAdministrator'
        db.delete_table('lizard_area_dataadministrator')

        # Deleting model 'AreaCode'
        db.delete_table('lizard_area_areacode')

        # Deleting model 'Status'
        db.delete_table('lizard_area_status')

        # Deleting model 'AreaType'
        db.delete_table('lizard_area_areatype')

        # Deleting model 'Province'
        db.delete_table('lizard_area_province')

        # Deleting model 'Municipality'
        db.delete_table('lizard_area_municipality')

        # Deleting model 'Basin'
        db.delete_table('lizard_area_basin')

        # Deleting model 'WaterManagementArea'
        db.delete_table('lizard_area_watermanagementarea')

        # Deleting model 'Communique'
        db.delete_table('lizard_area_communique')

        # Deleting model 'Area'
        db.delete_table('lizard_area_area')


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
        'lizard_area.areacode': {
            'Meta': {'object_name': 'AreaCode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_area.areatype': {
            'Meta': {'object_name': 'AreaType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_area.basin': {
            'Meta': {'object_name': 'Basin'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_area.category': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Category'},
            'geo_object_groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_area.GeoObjectGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapnik_xml_style_sheet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.MapnikXMLStyleSheet']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Category']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'lizard_area.communique': {
            'Meta': {'object_name': 'Communique', '_ormbases': ['lizard_area.GeoObject']},
            'area_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.AreaType']", 'null': 'True', 'blank': 'True'}),
            'basin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Basin']", 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.AreaCode']", 'null': 'True', 'blank': 'True'}),
            'geoobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lizard_area.GeoObject']", 'unique': 'True', 'primary_key': 'True'}),
            'municipality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Municipality']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Province']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Status']", 'null': 'True', 'blank': 'True'}),
            'watermanagementarea': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.WaterManagementArea']", 'null': 'True', 'blank': 'True'})
        },
        'lizard_area.dataadministrator': {
            'Meta': {'object_name': 'DataAdministrator'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_area.geoobject': {
            'Meta': {'object_name': 'GeoObject'},
            'geo_object_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.GeoObjectGroup']"}),
            'geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'})
        },
        'lizard_area.geoobjectgroup': {
            'Meta': {'object_name': 'GeoObjectGroup'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'source_log': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'lizard_area.mapnikxmlstylesheet': {
            'Meta': {'object_name': 'MapnikXMLStyleSheet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'source_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'style': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'})
        },
        'lizard_area.municipality': {
            'Meta': {'object_name': 'Municipality'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_area.province': {
            'Meta': {'object_name': 'Province'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_area.status': {
            'Meta': {'object_name': 'Status'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_area.watermanagementarea': {
            'Meta': {'object_name': 'WaterManagementArea'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        }
    }

    complete_apps = ['lizard_area']
