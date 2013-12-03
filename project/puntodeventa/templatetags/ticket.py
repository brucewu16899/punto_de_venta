from puntodeventa.models import Producto
from django import template
from django.conf import settings
IVA = settings.IVA
register = template.Library()

@register.filter(name='iva')
def iva(producto,ticket):
	producto = Producto.objects.filter(id=producto.id)[0]
	if producto.iva:
		iva = (((ticket.precio * ticket.cantidad) / (IVA+1)) * IVA)
	else:
		iva = 0
	return iva

@register.filter(name='total')
def total(precio, cantidad):
	return (precio * cantidad)