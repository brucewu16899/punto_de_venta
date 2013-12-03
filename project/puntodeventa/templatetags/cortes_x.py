# -*- encoding: utf-8 -*-
from puntodeventa.models import Corte, Corte_productos
from django import template
from django.conf import settings
IVA = settings.IVA
register = template.Library()

@register.filter(name='total')
def total(sucursal):
	try:
		corte = Corte.objects.filter(completado=False, sucursal=sucursal)[0]
		return corte.total
	except:
		return 0 

@register.filter(name='iva')
def iva(sucursal):
	try:
		corte = Corte.objects.filter(completado=False, sucursal=sucursal)[0]
		return corte.iva
	except:
		return 0 


@register.filter(name='productos')
def productos(sucursal):
	try:
		corte = Corte.objects.filter(completado=False, sucursal=sucursal.nombre)[0]
		corte_productos = Corte_productos.objects.filter(corte = corte)
		info = ''
		for registros in corte_productos:
			info = info + '<li><i class="icon-ok green"></i>'+ str(registros.cantidad) +' u. de '+ registros.producto +'&nbsp&nbsp&nbsp<strong class="text-right">$'+str('{:.2f}'.format(registros.total))+'</strong></li>'		
		return info

		
	except Exception, e:	
		info = "<li><i class='icon-remove red'></i> <strong>N/A</strong></li>" 
		return info


@register.filter(name='habilitar')
def habilitar(sucursal):
	corte = Corte.objects.filter(completado=False, sucursal=sucursal)
	if not corte:
		return 'disabled'
	else:
		return ''

@register.filter(name='folio_corte')
def folio_corte(sucursal):
	try:
		corte = Corte.objects.filter(completado=False, sucursal=sucursal)[0]
		return corte.folio
	except Exception, e:
		return '#'

