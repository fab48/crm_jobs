# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tecnologia'
        db.create_table(u'core_tecnologia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['Tecnologia'])

        # Adding model 'Desarrollador'
        db.create_table(u'core_desarrollador', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('perfil_github', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('perfil_linkedin', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('perfil_bitbucked', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('perfil_twitter', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'core', ['Desarrollador'])

        # Adding model 'Oferta'
        db.create_table(u'core_oferta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('empresa', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('salario', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('funciones', self.gf('django.db.models.fields.TextField')()),
            ('beneficios', self.gf('django.db.models.fields.TextField')()),
            ('estado', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Oferta'])

        # Adding M2M table for field aplicantes on 'Oferta'
        m2m_table_name = db.shorten_name(u'core_oferta_aplicantes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('oferta', models.ForeignKey(orm[u'core.oferta'], null=False)),
            ('desarrollador', models.ForeignKey(orm[u'core.desarrollador'], null=False))
        ))
        db.create_unique(m2m_table_name, ['oferta_id', 'desarrollador_id'])

        # Adding model 'TecnologiaOferta'
        db.create_table(u'core_tecnologiaoferta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tecnologia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Tecnologia'])),
            ('oferta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Oferta'])),
            ('nivel', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core', ['TecnologiaOferta'])

        # Adding model 'TecnologiaDesarrollador'
        db.create_table(u'core_tecnologiadesarrollador', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desarrollador', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Desarrollador'])),
            ('tecnologia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Tecnologia'])),
            ('nivel', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core', ['TecnologiaDesarrollador'])


    def backwards(self, orm):
        # Deleting model 'Tecnologia'
        db.delete_table(u'core_tecnologia')

        # Deleting model 'Desarrollador'
        db.delete_table(u'core_desarrollador')

        # Deleting model 'Oferta'
        db.delete_table(u'core_oferta')

        # Removing M2M table for field aplicantes on 'Oferta'
        db.delete_table(db.shorten_name(u'core_oferta_aplicantes'))

        # Deleting model 'TecnologiaOferta'
        db.delete_table(u'core_tecnologiaoferta')

        # Deleting model 'TecnologiaDesarrollador'
        db.delete_table(u'core_tecnologiadesarrollador')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
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
        u'core.desarrollador': {
            'Meta': {'object_name': 'Desarrollador'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'perfil_bitbucked': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'perfil_github': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'perfil_linkedin': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'perfil_twitter': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'tecnologias': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Tecnologia']", 'through': u"orm['core.TecnologiaDesarrollador']", 'symmetrical': 'False'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'core.oferta': {
            'Meta': {'object_name': 'Oferta'},
            'aplicantes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Desarrollador']", 'symmetrical': 'False'}),
            'beneficios': ('django.db.models.fields.TextField', [], {}),
            'empresa': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'estado': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'funciones': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'salario': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'tecnologias': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Tecnologia']", 'through': u"orm['core.TecnologiaOferta']", 'symmetrical': 'False'})
        },
        u'core.tecnologia': {
            'Meta': {'object_name': 'Tecnologia'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.tecnologiadesarrollador': {
            'Meta': {'object_name': 'TecnologiaDesarrollador'},
            'desarrollador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Desarrollador']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nivel': ('django.db.models.fields.IntegerField', [], {}),
            'tecnologia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Tecnologia']"})
        },
        u'core.tecnologiaoferta': {
            'Meta': {'object_name': 'TecnologiaOferta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nivel': ('django.db.models.fields.IntegerField', [], {}),
            'oferta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Oferta']"}),
            'tecnologia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Tecnologia']"})
        }
    }

    complete_apps = ['core']