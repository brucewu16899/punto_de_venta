# -*- encoding: utf-8 -*-
from django.db import models
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, _user_has_perm, PermissionsMixin, _user_has_module_perms
from datetime import datetime, time, date
from managers import UsuarioManager
from django.db.models.signals import *
from django.dispatch import receiver
from django.core.validators import RegexValidator
from project.settings.base import IVA

from slugify import slugify

Colores = (
	('f9f9f9', 'Default'),
    ('5090c1', 'Azul'),
    ('7d6eb0', 'Morado'),
    ('82af6f', 'Verde'),
    ('ffb95a', 'Naranja'),
    ('e04140', 'Rojo'),
    ('ffc557', 'Amarillo'),
    ('ce6f9e', 'Rosa'),
    ('848484', 'Gris'),    
)

class Menu(models.Model):

	nombre = models.CharField(max_length=20, unique=True)
	color = models.CharField(max_length=6, choices=Colores)
	slugify = models.CharField(max_length=20, unique=True)

	class Meta:
		ordering = ["nombre"]

	def __unicode__(self) :
	    return '%s' % (self.nombre)

@receiver(pre_save, sender=Menu)
def menu_pre_save(sender, instance, *args, **kwargs):

	menus = Menu.objects.all().order_by('nombre')
	for menu in menus:
		if menu.slugify == slugify(instance.nombre):
			instance.nombre = instance.nombre + 'x1'
			instance.save()
	instance.slugify = slugify(instance.nombre)

class Sucursal(models.Model):

	nombre = models.CharField(max_length=30, unique=True)
	color = models.CharField(max_length=6 ,choices=Colores)
	menu_principal = models.ForeignKey(Menu, blank=True, null=True, help_text='Es el menu por defecto al que lleva la primer pagina del vendedor')
	nombre_comercial = models.CharField(max_length=30, help_text='Nombre que aparece en el ticket')
	rfc = models.CharField(max_length=15, verbose_name="RFC")
	direccion = models.CharField(max_length=35)
	direccion2 = models.CharField(max_length=35,blank=True, verbose_name="Direccion")
	direccion3 = models.CharField(max_length=35,blank=True, verbose_name="Direccion")
	direccion4 = models.CharField(max_length=35,blank=True, verbose_name="Direccion")
	correo = models.EmailField(max_length=35,blank=True)
	telefono = models.CharField(max_length=15,blank=True)
	pagina = models.CharField(max_length=35,blank=True)

	def __unicode__(self) :
	    return '%s' % (self.nombre)

	class Meta:
  		verbose_name_plural = u'Sucursales'

Perfiles = (
	('vendedor', 'Vendedor'),
    ('autorizado para cobrar', 'Autorizado para cobrar'),
    ('cajero', 'Cajero'),
    ('supervisor', 'Supervisor'),
    ('administrador', 'Administrador'),
)

class Usuario(AbstractBaseUser, PermissionsMixin):

	usuario = models.CharField(max_length=25, unique=True, db_index=True)
	perfil  = models.CharField(max_length=25, choices=Perfiles)
	sucursal = models.ForeignKey(Sucursal, blank=True, null=True)
	codigo  = models.CharField(max_length=12, blank=True, validators=[RegexValidator(regex='^\d{12}$', message='El codigo debe ser de 12 caracteres y tener solo numeros', code='nomatch')], help_text="El codigo del supervisor para hacer un corte")
	activo = models.BooleanField(default=True, help_text='Activa un usuario para poder usar el sistema')
	administrador = models.BooleanField(default=False, help_text='Que usuarios se les permite entrar al administrador')
	supervisa = models.ManyToManyField(Sucursal, blank=True, null=True, related_name='supervisa_sucursal', help_text='Seleccione solo si el perfil es de Supervisor o de Administrador, ')
	objects = UsuarioManager()
	USERNAME_FIELD = 'usuario'

	unique_together = ("usuario", "codigo")
	
	def get_full_name(self):
		return self.usuario + ' ' + self.perfil

	def get_short_name(self):
		return self.usuario

	def __unicode__(self):
		return self.usuario

	def has_perm(self, perm, obj=None):
		if self.is_superuser:
			return True
		return _user_has_perm(self, perm, obj=obj)

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.administrador

	@property
	def is_active(self):
		return self.activo
			
def usuario_post_save1(sender, instance, action, **kwargs):
	if  instance.perfil != 'administrador' and instance.perfil != 'supervisor':
		if action == 'post_add':
			instance.supervisa = []
			instance.save()
		if action == 'post_remove':
			instance.supervisa = []
			instance.save()

m2m_changed.connect(usuario_post_save1, sender=Usuario.supervisa.through)

class Producto(models.Model):
	menu = models.ForeignKey(Menu)
	sucursal = models.ManyToManyField(Sucursal, help_text="Puede elegir entre uno o varias sucursales.")
	nombre = models.CharField(max_length=20, unique=True)
	alias = models.CharField(max_length=30, blank=True , help_text="Nombre del producto en el ticket, si lo quiere mantener deja vacio este campo")
	precio = models.FloatField(default=0)
	iva = models.BooleanField(default=False, help_text="Habilita si el precio incluye "+str(IVA)+" porc. de iva")
	principal = models.BooleanField(default=False, help_text="Habilita si el producto es muy vendido")
	precio_dinamico = models.BooleanField('Precio dinámico',default=False, help_text="Habilita esta opcion si el producto cambia de precio constantemente")
	codigo = models.CharField('Codigo de barras',max_length=25, default='0')

	class Meta:
		ordering = ["nombre"]
		
       	

	def __unicode__(self) :
	    return '%s' % (self.nombre)

class Productosucursal(models.Model):

	producto = models.ForeignKey(Producto)
	sucursal = models.ForeignKey(Sucursal)
	inventario = models.IntegerField('inventario', default='0')
	merma = models.IntegerField('Desperdicio', default='0')

	class Meta:
		ordering = ["producto"]

	def __unicode__(self) :
	    return '%s' % (self.producto)

	class Meta:
  		verbose_name_plural = u'Inventarios'
  		verbose_name=u'inventario'

def producto_post_save(sender, instance, action, **kwargs):
	if action == 'post_add':
		productos_sucursal = Productosucursal.objects.filter(producto = instance)
		for productos in productos_sucursal:
			if not productos.sucursal in instance.sucursal.all():
				productos.delete()
		for sucursal in instance.sucursal.all():
			productos_sucursal = Productosucursal.objects.filter(producto = instance, sucursal = sucursal)
			if not productos_sucursal:
				productos_sucursal_crear = Productosucursal()
				productos_sucursal_crear.producto = instance
				productos_sucursal_crear.sucursal = sucursal
				productos_sucursal_crear.save()
	if not instance.alias:
		instance.alias = instance.nombre
		instance.save()

m2m_changed.connect(producto_post_save, sender=Producto.sucursal.through)

@receiver(post_delete, sender=Producto)
def producto_post_delete(sender, instance, *args, **kwargs):
	Productosucursal.objects.filter(producto = instance).delete()

class Ticket_actual(models.Model):

	producto = models.ForeignKey(Producto)
	vendedor = models.ForeignKey(Usuario)
	cantidad = models.IntegerField(default=0)
	sucursal = models.ForeignKey(Sucursal)
	precio = models.FloatField(default=0)

	def __unicode__(self) :
		return '%s' % (self.producto)

	class Meta:
		ordering = ["-id"]

Estatus_ticket = (
	('pendiente', 'Pendiente'),
    ('cobrado', 'Cobrado'),
    ('cortado', 'Cortado'),
    ('facturado', 'Facturado'),
    ('oculto', 'Oculto'),
)

class Ticket(models.Model):

	folio = models.CharField(max_length=20)
	sucursal = models.CharField(max_length=40)
	total = models.FloatField(default=0)
	iva = models.FloatField(default=0)
	vendedor = models.CharField(max_length=50)
	estatus = models.CharField(max_length=50,choices=Estatus_ticket)
	fecha = models.DateField(auto_now_add=True)
	hora = models.TimeField(auto_now_add=True)
	corte = models.CharField(max_length=20, default = '0')

	def __unicode__(self) :
		return '%s' % (self.folio)

	class Meta:
		ordering = ["-fecha","-hora"]

@receiver(pre_delete, sender=Ticket)
def menu_pre_delete(sender, instance, *args, **kwargs):

	if instance.estatus == 'cobrado':
		ticket_productos = Ticket_productos.objects.filter(ticket=instance).distinct()
		corte = Corte.objects.filter(folio = instance.corte)[0]
		for ticket_producto in ticket_productos:
			producto = Productosucursal.objects.filter(producto__nombre = ticket_producto.producto, sucursal__nombre = instance.sucursal)[0]
			producto.inventario = producto.inventario + ticket_producto.cantidad
			producto.save()

			corte.total = corte.total - ticket_producto.total
			corte.iva = corte.iva - ticket_producto.iva
			
			corte_productos = Corte_productos.objects.filter(corte = corte, producto = ticket_producto.producto, precio=ticket_producto.precio)[0]
			corte_productos.cantidad = corte_productos.cantidad - ticket_producto.cantidad
			corte_productos.total = corte_productos.total - ticket_producto.total
			corte_productos.iva = corte_productos.iva - ticket_producto.iva
			corte_productos.save()

			if corte_productos.cantidad <= 0:
				corte_productos.delete()

		corte.save()

	elif instance.estatus == 'cortado' or instance.estatus == 'facturado' or instance.estatus == 'oculto':
		raise Exception('No puedes eliminar un ticket con este estatus')

class Ticket_productos(models.Model):

	ticket = models.ForeignKey(Ticket)
	producto = models.CharField(max_length=40)
	alias = models.CharField(max_length=40)
	cantidad = models.IntegerField(default=0)
	precio = models.FloatField(default=0)
	total = models.FloatField(default=0)
	iva = models.FloatField(default=0)

	def __unicode__(self) :
		return '%s' % (self.ticket)

	class Meta:
		ordering = ["ticket"]

class Corte(models.Model):

	folio = models.CharField(max_length=20)
	total = models.FloatField(default=0)
	iva = models.FloatField(default=0)
	fecha = models.DateField(auto_now_add=True)
	hora = models.TimeField(auto_now_add=True)
	sucursal = models.CharField(max_length=40)
	completado = models.BooleanField(default=False)
	facturado = models.BooleanField(default=False)

	def __unicode__(self) :
		return '%s' % (self.folio)
	
	def Numero_de_clientes(self):
		clientes = 	Ticket.objects.filter(corte = self.folio)
		return len(clientes)	
	
	def Ultimo_ticket(self):
		try :
			ultimo = Ticket.objects.filter(corte = self.folio)[0].hora
		except:
			ultimo = False
		return ultimo
		
	class Meta:
		ordering = ["-folio"]

class Corte_productos(models.Model):

	corte = models.ForeignKey(Corte)
	producto = models.CharField(max_length=40)
	cantidad = models.IntegerField(default=0)
	precio = models.FloatField(default=0)
	total = models.FloatField(default=0)
	iva = models.FloatField(default=0)

	def __unicode__(self) :
		return '%s' % (self.corte)

	class Meta:
		ordering = ["-corte"]
