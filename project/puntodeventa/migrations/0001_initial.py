# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Menu'
        db.create_table(u'puntodeventa_menu', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('slugify', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal(u'puntodeventa', ['Menu'])

        # Adding model 'Sucursal'
        db.create_table(u'puntodeventa_sucursal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('menu_principal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['puntodeventa.Menu'], null=True, blank=True)),
            ('nombre_comercial', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('rfc', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('direccion2', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('direccion3', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('direccion4', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('correo', self.gf('django.db.models.fields.EmailField')(max_length=35, blank=True)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('pagina', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
        ))
        db.send_create_signal(u'puntodeventa', ['Sucursal'])

        # Adding model 'Usuario'
        db.create_table(u'puntodeventa_usuario', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('usuario', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25, db_index=True)),
            ('perfil', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('sucursal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['puntodeventa.Sucursal'], null=True, blank=True)),
            ('codigo', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('administrador', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'puntodeventa', ['Usuario'])

        # Adding M2M table for field groups on 'Usuario'
        m2m_table_name = db.shorten_name(u'puntodeventa_usuario_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usuario', models.ForeignKey(orm[u'puntodeventa.usuario'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['usuario_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Usuario'
        m2m_table_name = db.shorten_name(u'puntodeventa_usuario_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usuario', models.ForeignKey(orm[u'puntodeventa.usuario'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['usuario_id', 'permission_id'])

        # Adding M2M table for field supervisa on 'Usuario'
        m2m_table_name = db.shorten_name(u'puntodeventa_usuario_supervisa')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usuario', models.ForeignKey(orm[u'puntodeventa.usuario'], null=False)),
            ('sucursal', models.ForeignKey(orm[u'puntodeventa.sucursal'], null=False))
        ))
        db.create_unique(m2m_table_name, ['usuario_id', 'sucursal_id'])

        # Adding model 'Producto'
        db.create_table(u'puntodeventa_producto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['puntodeventa.Menu'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('precio', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('iva', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('principal', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('precio_dinamico', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('codigo', self.gf('django.db.models.fields.CharField')(default='0', max_length=25)),
        ))
        db.send_create_signal(u'puntodeventa', ['Producto'])

        # Adding M2M table for field sucursal on 'Producto'
        m2m_table_name = db.shorten_name(u'puntodeventa_producto_sucursal')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('producto', models.ForeignKey(orm[u'puntodeventa.producto'], null=False)),
            ('sucursal', models.ForeignKey(orm[u'puntodeventa.sucursal'], null=False))
        ))
        db.create_unique(m2m_table_name, ['producto_id', 'sucursal_id'])

        # Adding model 'Productosucursal'
        db.create_table(u'puntodeventa_productosucursal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['puntodeventa.Producto'])),
            ('sucursal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['puntodeventa.Sucursal'])),
            ('inventario', self.gf('django.db.models.fields.IntegerField')(default='0')),
            ('merma', self.gf('django.db.models.fields.IntegerField')(default='0')),
        ))
        db.send_create_signal(u'puntodeventa', ['Productosucursal'])

        # Adding model 'Ticket_actual'
        db.create_table(u'puntodeventa_ticket_actual', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['puntodeventa.Producto'])),
            ('vendedor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['puntodeventa.Usuario'])),
            ('cantidad', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sucursal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['puntodeventa.Sucursal'])),
            ('precio', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal(u'puntodeventa', ['Ticket_actual'])

        # Adding model 'Ticket'
        db.create_table(u'puntodeventa_ticket', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('folio', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('sucursal', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('total', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('iva', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('vendedor', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('estatus', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('fecha', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('hora', self.gf('django.db.models.fields.TimeField')(auto_now_add=True, blank=True)),
            ('corte', self.gf('django.db.models.fields.CharField')(default='0', max_length=20)),
        ))
        db.send_create_signal(u'puntodeventa', ['Ticket'])

        # Adding model 'Ticket_productos'
        db.create_table(u'puntodeventa_ticket_productos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ticket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['puntodeventa.Ticket'])),
            ('producto', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('cantidad', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('precio', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('total', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('iva', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal(u'puntodeventa', ['Ticket_productos'])

        # Adding model 'Corte'
        db.create_table(u'puntodeventa_corte', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('folio', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('total', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('iva', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('fecha', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('hora', self.gf('django.db.models.fields.TimeField')(auto_now_add=True, blank=True)),
            ('sucursal', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('completado', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('facturado', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'puntodeventa', ['Corte'])

        # Adding model 'Corte_productos'
        db.create_table(u'puntodeventa_corte_productos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('corte', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['puntodeventa.Corte'])),
            ('producto', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('cantidad', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('precio', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('total', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('iva', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal(u'puntodeventa', ['Corte_productos'])


    def backwards(self, orm):
        # Deleting model 'Menu'
        db.delete_table(u'puntodeventa_menu')

        # Deleting model 'Sucursal'
        db.delete_table(u'puntodeventa_sucursal')

        # Deleting model 'Usuario'
        db.delete_table(u'puntodeventa_usuario')

        # Removing M2M table for field groups on 'Usuario'
        db.delete_table(db.shorten_name(u'puntodeventa_usuario_groups'))

        # Removing M2M table for field user_permissions on 'Usuario'
        db.delete_table(db.shorten_name(u'puntodeventa_usuario_user_permissions'))

        # Removing M2M table for field supervisa on 'Usuario'
        db.delete_table(db.shorten_name(u'puntodeventa_usuario_supervisa'))

        # Deleting model 'Producto'
        db.delete_table(u'puntodeventa_producto')

        # Removing M2M table for field sucursal on 'Producto'
        db.delete_table(db.shorten_name(u'puntodeventa_producto_sucursal'))

        # Deleting model 'Productosucursal'
        db.delete_table(u'puntodeventa_productosucursal')

        # Deleting model 'Ticket_actual'
        db.delete_table(u'puntodeventa_ticket_actual')

        # Deleting model 'Ticket'
        db.delete_table(u'puntodeventa_ticket')

        # Deleting model 'Ticket_productos'
        db.delete_table(u'puntodeventa_ticket_productos')

        # Deleting model 'Corte'
        db.delete_table(u'puntodeventa_corte')

        # Deleting model 'Corte_productos'
        db.delete_table(u'puntodeventa_corte_productos')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'puntodeventa.corte': {
            'Meta': {'ordering': "['-folio']", 'object_name': 'Corte'},
            'completado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facturado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'folio': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'hora': ('django.db.models.fields.TimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iva': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'sucursal': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'total': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'puntodeventa.corte_productos': {
            'Meta': {'ordering': "['-corte']", 'object_name': 'Corte_productos'},
            'cantidad': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'corte': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['puntodeventa.Corte']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iva': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'precio': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'producto': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'total': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'puntodeventa.menu': {
            'Meta': {'ordering': "['nombre']", 'object_name': 'Menu'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'slugify': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'puntodeventa.producto': {
            'Meta': {'ordering': "['nombre']", 'object_name': 'Producto'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'codigo': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iva': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['puntodeventa.Menu']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'precio': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'precio_dinamico': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'principal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sucursal': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['puntodeventa.Sucursal']", 'symmetrical': 'False'})
        },
        u'puntodeventa.productosucursal': {
            'Meta': {'object_name': 'Productosucursal'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventario': ('django.db.models.fields.IntegerField', [], {'default': "'0'"}),
            'merma': ('django.db.models.fields.IntegerField', [], {'default': "'0'"}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['puntodeventa.Producto']"}),
            'sucursal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['puntodeventa.Sucursal']"})
        },
        u'puntodeventa.sucursal': {
            'Meta': {'object_name': 'Sucursal'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'correo': ('django.db.models.fields.EmailField', [], {'max_length': '35', 'blank': 'True'}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'direccion2': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'direccion3': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'direccion4': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_principal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['puntodeventa.Menu']", 'null': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'nombre_comercial': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'pagina': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'rfc': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        },
        u'puntodeventa.ticket': {
            'Meta': {'ordering': "['-fecha', '-hora']", 'object_name': 'Ticket'},
            'corte': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '20'}),
            'estatus': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'folio': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'hora': ('django.db.models.fields.TimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iva': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'sucursal': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'total': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'vendedor': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'puntodeventa.ticket_actual': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Ticket_actual'},
            'cantidad': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'precio': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['puntodeventa.Producto']"}),
            'sucursal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['puntodeventa.Sucursal']"}),
            'vendedor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['puntodeventa.Usuario']"})
        },
        u'puntodeventa.ticket_productos': {
            'Meta': {'ordering': "['ticket']", 'object_name': 'Ticket_productos'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'cantidad': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iva': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'precio': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'producto': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'ticket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['puntodeventa.Ticket']"}),
            'total': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'puntodeventa.usuario': {
            'Meta': {'object_name': 'Usuario'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'administrador': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'perfil': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'sucursal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['puntodeventa.Sucursal']", 'null': 'True', 'blank': 'True'}),
            'supervisa': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'supervisa_sucursal'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['puntodeventa.Sucursal']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'usuario': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25', 'db_index': 'True'})
        }
    }

    complete_apps = ['puntodeventa']