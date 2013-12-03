# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.db import connection, transaction
from forms import *
from models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from django.utils import simplejson
from django.conf import settings
EMPRESA = settings.EMPRESA
VENCE = settings.VENCE
IVA = settings.IVA
IPDJANGO = settings.IPDJANGO
PORTDJANGO = settings.PORTDJANGO
IPNODE = settings.IPNODE
PORTNODE = settings.PORTNODE

def inicio(request):

	empresa = EMPRESA
	formulario = InicioForm()
	error = []
	if not request.user.is_anonymous():
		hoy = datetime.date(datetime.now())
		if hoy > VENCE:
			error.append("Periodo de sistema expirado")
			logout(request)
		else:
			usuario = request.user
			if usuario.perfil == 'vendedor' or usuario.perfil == 'autorizado para cobrar':
				try:
					menu = usuario.sucursal.menu_principal				
					return HttpResponseRedirect(reverse('vendedor', args=[menu.slugify]))
				except:
					mensaje = []
					mensaje.append('No hay menus o productos asignados')
					return render(request, 'blank.html',locals())					
			elif usuario.perfil == 'cajero':
				return HttpResponseRedirect(reverse('caja'))
			elif usuario.perfil == 'supervisor':
				return HttpResponseRedirect(reverse('sucursales'))
			elif usuario.perfil == 'administrador':
				return HttpResponseRedirect(reverse('sucursales'))

	if request.method == "POST":
		formulario = InicioForm(request.POST)
		if formulario.is_valid():
			usuario = formulario.cleaned_data["usuario"]
			password = formulario.cleaned_data["password"]
			acceso = authenticate(username=str(usuario), password=str(password))
			if acceso is not None:			
				if acceso.is_active:
					login(request, acceso)
					usuario = request.user
					return HttpResponseRedirect(reverse('inicio'))
				else:
					error.append("Tu usuario esta desactivado")		
			else:
				error.append('Usuario o contraseña incorrecta')
		else:
			error.append('Usuario o contraseña incorrecta')
	return render(request, 'login.html',locals())

def salir(request):
	logout(request)
	return HttpResponseRedirect(reverse('inicio'))

def vendedor(request,menuid):

	usuario, empresa = request.user , EMPRESA
	menus = []
	mensaje = [] 	

	productos = Producto.objects.filter(sucursal=usuario.sucursal).distinct()

	if not productos:
		mensaje.append('No hay productos que mostrar')
		return render(request, 'blank.html',locals())

	for producto in productos:
		if not producto.menu in menus:
			menus.append(producto.menu)

	principales = Producto.objects.filter(sucursal=usuario.sucursal, principal=True)
	productos = Producto.objects.filter(sucursal=usuario.sucursal, menu__slugify=menuid)
	tickets = Ticket_actual.objects.filter(vendedor=usuario, sucursal=usuario.sucursal).distinct()

	if tickets:
		total = 0
		cantidad = 0 
		for registro in tickets:
			total = total + (registro.precio * registro.cantidad)
			cantidad = cantidad + registro.cantidad

	return render(request, 'vendedor.html',locals())

def validar_ticket(request):

	producto = request.POST['producto']
	cantidad = request.POST['cantidad']
	usuario = request.user

	if producto == 'cancelar_ticket':
		Ticket_actual.objects.filter(vendedor = usuario, sucursal=usuario.sucursal).delete()
		datos = {'cancelar_ticket':True}
		http_response = HttpResponse(json.dumps(datos),mimetype='application/json')
		return http_response

	producto = Producto.objects.filter(id = producto)[0]

	if not cantidad:
		cantidad = 1
	elif cantidad <= 0:
		cantidad = 1

	if producto.precio_dinamico:
		ticket_actual = Ticket_actual.objects.filter(producto = producto, vendedor = usuario, sucursal=usuario.sucursal, precio=cantidad).distinct()
		if ticket_actual:
			ticket_actual[0].cantidad = ticket_actual[0].cantidad + 1
			ticket_actual[0].save()
		else:
			ticket_actual = Ticket_actual()
			ticket_actual.producto = producto
			ticket_actual.vendedor = usuario
			ticket_actual.cantidad = 1
			ticket_actual.sucursal = usuario.sucursal
			ticket_actual.precio = cantidad
			ticket_actual.save()
	else:
		cantidad = int(float(cantidad))
		ticket_actual = Ticket_actual.objects.filter(producto = producto, vendedor = usuario, sucursal=usuario.sucursal).distinct()
		if ticket_actual:
			ticket_actual[0].cantidad = ticket_actual[0].cantidad + cantidad
			ticket_actual[0].save()
		else:
			ticket_actual = Ticket_actual()
			ticket_actual.producto = producto
			ticket_actual.vendedor = usuario
			ticket_actual.cantidad = cantidad
			ticket_actual.sucursal = usuario.sucursal
			ticket_actual.precio = producto.precio
			ticket_actual.save()	

	tickets = Ticket_actual.objects.filter(vendedor = usuario, sucursal=usuario.sucursal).distinct()
	ticket = []
	total = 0
	cantidad = 0 
	if tickets:
		for registro in tickets:
			ticket.append(str(registro.cantidad) + ' u de ' + registro.producto.nombre)
			total = total + (registro.precio * registro.cantidad)
			cantidad = cantidad + registro.cantidad

	datos = {'ticket':ticket,'total':total,'cantidad':cantidad,'agregar_registro':True}

	http_response = HttpResponse(json.dumps(datos),mimetype='application/json')	
	return http_response

def validar_codigo(request):
	codigo = request.POST['codigo']
	cantidad = request.POST['cantidad']
	usuario = request.user

	if not codigo or codigo == '0':
		datos = {'error_codigo':True,'mensaje':'No haz introducido ningun codigo'}
		http_response = HttpResponse(json.dumps(datos),mimetype='application/json')
		return http_response

	try:
		producto = Producto.objects.filter(codigo = codigo)[0]
	except:
		datos = {'error_codigo':True,'mensaje':'No se encontro tu codigo'}
		http_response = HttpResponse(json.dumps(datos),mimetype='application/json')
		return http_response

	if producto.precio_dinamico:

		if not cantidad:
			cantidad = 1
		elif cantidad <= 0:
			cantidad = 1

		ticket_actual = Ticket_actual.objects.filter(producto = producto, vendedor = usuario, sucursal=usuario.sucursal, precio=cantidad).distinct()
		if ticket_actual:
			ticket_actual[0].cantidad = ticket_actual[0].cantidad + 1
			ticket_actual[0].save()
		else:
			ticket_actual = Ticket_actual()
			ticket_actual.producto = producto
			ticket_actual.vendedor = usuario
			ticket_actual.cantidad = 1
			ticket_actual.sucursal = usuario.sucursal
			ticket_actual.precio = cantidad
			ticket_actual.save()
			
	else:
		ticket_actual = Ticket_actual.objects.filter(producto = producto, vendedor = usuario, sucursal=usuario.sucursal).distinct()
		if ticket_actual:
			ticket_actual[0].cantidad = ticket_actual[0].cantidad + 1
			ticket_actual[0].save()
		else:
			ticket_actual = Ticket_actual()
			ticket_actual.producto = producto
			ticket_actual.vendedor = usuario
			ticket_actual.cantidad = 1
			ticket_actual.sucursal = usuario.sucursal
			ticket_actual.precio = producto.precio
			ticket_actual.save()
		
	tickets = Ticket_actual.objects.filter(vendedor = usuario, sucursal=usuario.sucursal).distinct()
	ticket = []
	total = 0
	cantidad = 0 
	if tickets:
		for registro in tickets:
			ticket.append(str(registro.cantidad) + ' u de ' + registro.producto.nombre)
			total = total + (registro.precio * registro.cantidad)
			cantidad = cantidad + registro.cantidad

	datos = {'ticket':ticket,'total':total,'cantidad':cantidad,'agregar_registro':True}

	http_response = HttpResponse(json.dumps(datos),mimetype='application/json')	
	return http_response

def imprimir_ticket(request):
	usuario, ipdjango, portdjango, ipnode, portnode = request.user, IPDJANGO, PORTDJANGO, IPNODE, PORTNODE
	tickets = Ticket_actual.objects.filter(vendedor = usuario, sucursal=usuario.sucursal).distinct()
	if tickets:

		total = 0
		iva = 0
		try:
			folio = Ticket.objects.all().order_by('-folio')[0]
			folio = str(int(folio.folio)+ 1)					
		except:		
			folio = '100000000000'
	
		crear_ticket = Ticket()
		crear_ticket.folio = folio
		crear_ticket.sucursal = usuario.sucursal.nombre
		crear_ticket.vendedor = usuario.usuario
		
		if usuario.perfil == 'autorizado para cobrar':
			crear_ticket.estatus = 'cobrado'
		else:
			crear_ticket.estatus = 'pendiente'

		crear_ticket.save()
		ticket_consulta = Ticket.objects.filter(folio = folio)[0]

		for registro in tickets:

			total =  total + (registro.precio * registro.cantidad)
			if registro.producto.iva:
				iva = iva + (((registro.precio * registro.cantidad) / (IVA+1)) * IVA)

			crear_ticket_producto = Ticket_productos()
			crear_ticket_producto.ticket = ticket_consulta
			crear_ticket_producto.producto = registro.producto.nombre
			crear_ticket_producto.alias = registro.producto.alias
			crear_ticket_producto.precio = registro.precio
			crear_ticket_producto.cantidad = registro.cantidad
			crear_ticket_producto.total = registro.precio * registro.cantidad
			if registro.producto.iva:
				crear_ticket_producto.iva = (((registro.precio * registro.cantidad) / (IVA+1)) * IVA)
			crear_ticket_producto.save()

			if usuario.perfil == 'autorizado para cobrar':
				sucursal = Sucursal.objects.filter(id = usuario.sucursal.id)[0]

				try:
					corte = Corte.objects.filter(sucursal=sucursal.nombre, completado = False)[0]
					_folio = corte.folio 
				except:
					try:
						corte = Corte.objects.all().order_by('-folio')[0]
						_folio = int(corte.folio) + 1
					except:
						_folio = 100000000000

					corte = Corte()
					corte.folio = _folio
					corte.sucursal = usuario.sucursal.nombre
					corte.save()

				try:
					corte_productos = Corte_productos.objects.filter(corte = corte, producto = registro.producto, precio = registro.precio)[0]
					corte_productos.cantidad = corte_productos.cantidad + registro.cantidad
					corte_productos.total = corte_productos.total + (registro.precio * registro.cantidad)
					if registro.producto.iva:
						corte_productos.iva = corte_productos.iva + ((((registro.precio * registro.cantidad) / (IVA+1)) * IVA))
					corte_productos.save()				

				except:
					corte_productos = Corte_productos()
					corte_productos.corte = corte
					corte_productos.producto = registro.producto 
					corte_productos.cantidad = registro.cantidad
					corte_productos.precio = registro.precio
					corte_productos.total = registro.precio * registro.cantidad
					if registro.producto.iva:
						corte_productos.iva = (((registro.precio * registro.cantidad) / (IVA+1)) * IVA)
					corte_productos.save()

				producto_sucursal = Productosucursal.objects.filter(producto = registro.producto, sucursal = sucursal)[0]
				producto_sucursal.inventario = producto_sucursal.inventario - registro.cantidad
				producto_sucursal.save()
				crear_ticket.corte = _folio

		subtotal = total - iva
		crear_ticket.total = total
		crear_ticket.iva = iva

		crear_ticket.save()

		if usuario.perfil == 'autorizado para cobrar':
			corte.total = corte.total + total
			corte.iva = corte.iva + iva
			corte.save()

		Ticket_actual.objects.filter(vendedor = usuario, sucursal=usuario.sucursal).delete()	
		return render(request, 'ticket.html',locals())

	else:
		mensaje=[]
		mensaje.append('No hay productos actualmente')
		return render(request, 'blank.html',locals())

def caja(request):
	usuario, empresa, ipdjango, portdjango, ipnode, portnode = request.user , EMPRESA, IPDJANGO, PORTDJANGO, IPNODE, PORTNODE 
	pendientes = Ticket.objects.filter(sucursal = usuario.sucursal.nombre, estatus = 'pendiente')
	cobrados = Ticket.objects.filter(sucursal = usuario.sucursal.nombre, estatus = 'cobrado')

	return render(request, 'caja.html',locals())

def cobrar(request):
	usuario = request.user
	folio = request.POST['folio']
	try:
		ticket =  Ticket.objects.filter(folio=folio , estatus='pendiente')[0]
		sucursal = Sucursal.objects.filter(id = usuario.sucursal.id)[0]

		if sucursal.nombre != ticket.sucursal:
			datos = {'folio':folio,'cobrado':False,'mensaje':'Este ticket no pertenece a esta sucursal, se notificara el incidente'}
			http_response = HttpResponse(json.dumps(datos),mimetype='application/json')
			return http_response

		try:
			corte = Corte.objects.filter(sucursal=sucursal.nombre, completado = False)[0]
			_folio = corte.folio
		except:
			try:
				corte = Corte.objects.all().order_by('-folio')[0]
				_folio = int(corte.folio) + 1
			except:
				_folio = 100000000000

			corte = Corte()
			corte.folio = _folio
			corte.sucursal = usuario.sucursal.nombre
			corte.save()

		registros = Ticket_productos.objects.filter(ticket=ticket)
		for registro in registros:
			producto = Productosucursal.objects.filter(producto__nombre = registro.producto, sucursal = sucursal)[0]
			producto.inventario = producto.inventario - registro.cantidad
			producto.save()

			try:
				corte_productos = Corte_productos.objects.filter(corte = corte, producto = registro.producto, precio = registro.precio)[0]
				corte_productos.cantidad = corte_productos.cantidad + registro.cantidad
				corte_productos.total = corte_productos.total + registro.total
				corte_productos.iva = corte_productos.iva + registro.iva
				corte_productos.save()				

			except:
				corte_productos = Corte_productos()
				corte_productos.corte = corte
				corte_productos.producto = registro.producto 
				corte_productos.cantidad = registro.cantidad
				corte_productos.precio = registro.precio
				corte_productos.total = registro.total
				corte_productos.iva = registro.iva
				corte_productos.save()
				
		corte.total = corte.total + ticket.total
		corte.iva = corte.iva + ticket.iva
		corte.save()

		ticket.estatus = 'cobrado'
		ticket.corte = _folio
		ticket.save()
		datos = {'folio':ticket.folio,'total':ticket.total,'vendedor':ticket.vendedor,'hora':ticket.hora.strftime("%H:%M"),'cobrado':True}
		http_response = HttpResponse(json.dumps(datos),mimetype='application/json')
		return http_response

	except Exception, e:
		datos = {'folio':folio,'cobrado':False,'mensaje':str(e)}
		http_response = HttpResponse(json.dumps(datos),mimetype='application/json')
		return http_response

@csrf_exempt
def node_js_ticket(request):
	username = request.POST['username']
	usuario = Usuario.objects.filter(id = username)[0]
	ticket = Ticket.objects.all().order_by('-folio')[0]
	hora = ticket.hora.strftime("%H:%M")
	data = {'ticket':True, 'folio': ticket.folio, 'cantidad': ticket.total, 'vendedor': ticket.vendedor, 'hora': hora, 'estatus': ticket.estatus, 'sucursal': ticket.sucursal}
	return HttpResponse(json.dumps(data), mimetype="application/json")

def sucursales(request):
	usuario, empresa = request.user , EMPRESA
	sucursales = usuario.supervisa.all()

	return render(request, 'sucursales.html',locals())


def cortez(request):
	sucursal = request.POST['cortez']
	sucursal = Sucursal.objects.filter(id=sucursal)[0]
	usuario = request.user

	try:
		corte = Corte.objects.filter(sucursal=sucursal.nombre, completado=False)[0]
		ticket = Ticket.objects.filter(corte = corte.folio)
		for registro in ticket:
			registro.estatus = 'cortado'
			registro.save()
		corte.completado = True
		corte.save()
	
	except Exception, e:
		print e
		datos = {'error':'No hay productos para realizar un corte'}
		http_response = HttpResponse(json.dumps(datos),mimetype='application/json')
		return http_response
	
	datos = {'sucursal':sucursal.nombre}
	http_response = HttpResponse(json.dumps(datos),mimetype='application/json')
	return http_response

def cortes(request):
	usuario, empresa = request.user , EMPRESA
	cortes = Corte.objects.filter(sucursal__in = usuario.supervisa.all().values_list('nombre'), completado=True)
	return render(request, 'cortes.html',locals())

def corte_consulta(request, folio):
	usuario, empresa = request.user , EMPRESA
	corte = Corte.objects.filter(folio=folio)[0]
	corte_productos = Corte_productos.objects.filter(corte=corte)
	sucursal = Sucursal.objects.filter(nombre = corte.sucursal)[0]
	subtotal = corte.total - corte.iva
	tickets = Ticket.objects.filter(corte = folio).exclude(estatus='oculto')
	return render(request, 'corte_consulta.html',locals())

def rasurado(request):
	usuario = request.user

	if not usuario.perfil == 'administrador':
		datos = {'error':True, 'mensaje':'Solo un administrador puede realizar esta tarea el insidente sera reportado'}
		http_response = HttpResponse(json.dumps(datos),mimetype='application/json')
		return http_response

	corte = request.POST['rasurado']
	corte = Corte.objects.filter(id=corte)[0]

	try:
		cantidad = request.POST['cantidad']
		cantidad = int(cantidad)
		if (corte.total - corte.total/3) > cantidad :
			datos = {'error':True, 'mensaje':'Valor demaciado pequeño'}
			http_response = HttpResponse(json.dumps(datos),mimetype='application/json')
			return http_response

	except Exception, e:
		print e
		datos = {'error':True, 'mensaje':'La cantidad introducida no es valida'}
		http_response = HttpResponse(json.dumps(datos),mimetype='application/json')
		return http_response

	tickets = Ticket.objects.filter(corte = corte.folio).order_by('-total')
	for ticket in tickets:
		
		ticket_productos = Ticket_productos.objects.filter(ticket=ticket)
		for ticket_producto in ticket_productos:
			corte_productos = Corte_productos.objects.filter(corte = corte, producto = ticket_producto.producto, precio = ticket_producto.precio)[0]
			corte_productos.cantidad = corte_productos.cantidad - ticket_producto.cantidad
			corte_productos.total = corte_productos.total - ticket_producto.total
			corte_productos.iva = corte_productos.iva - ticket_producto.iva
			corte_productos.save()

			if corte_productos.cantidad <= 0:
				corte_productos.delete()

		corte.total = corte.total - ticket.total
		corte.iva = corte.iva - ticket.iva
		corte.save()

		ticket.estatus = 'oculto'
		ticket.save()

		if corte.total <= cantidad:
			break
			
	#Cortes Reales
	corte.total = request.POST['cantidad']
	corte.save()
			 	
	datos = {'error':False, 'mensaje':'Todo bien'}
	http_response = HttpResponse(json.dumps(datos),mimetype='application/json')
	return http_response

def validar_supervisor(request):
	usuario = request.user
	codigo = request.POST['pass']
	supervisor = Usuario.objects.filter(Q(perfil='supervisor') | Q(perfil='administrador'), codigo = codigo)
	if supervisor:
		corte = Corte.objects.filter(sucursal = usuario.sucursal.nombre, completado=False)
		if not corte:
			datos = {'corte':False, 'mensaje':'No hay productos para hacer un corte'}
			http_response = HttpResponse(json.dumps(datos),mimetype='application/json')
			return http_response
		datos = {'corte':True, 'folio':corte[0].folio}
		http_response = HttpResponse(json.dumps(datos),mimetype='application/json')
		return http_response
	else:
		datos = {'corte':False, 'mensaje':'No estas autorizado, se reportara el incidente'}
		http_response = HttpResponse(json.dumps(datos),mimetype='application/json')
		return http_response

def reset(request):
     cursor = connection.cursor()
     cursor.execute("SELECT setval('puntodeventa_productosucursal_id_seq', (110)+1)")
     success = simplejson.dumps({'success':'success',})
     return HttpResponse(success, mimetype='application/json') 

