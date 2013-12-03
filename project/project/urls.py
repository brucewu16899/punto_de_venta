#encoding:utf-8
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()
from django.conf import settings

urlpatterns = patterns('',

  # Uncomment the next line to enable the admin:
  url(r'^$', 'puntodeventa.views.inicio', name='inicio'),
  url(r'^inicio/$', 'puntodeventa.views.inicio', name='inicio'),
  url(r'^salir/$', 'puntodeventa.views.salir', name='salir'),
  url(r'^vendedor/(.+)/$', 'puntodeventa.views.vendedor', name='vendedor'),
  url(r'^validar-ticket/$', 'puntodeventa.views.validar_ticket', name='validar_ticket'),
  url(r'^validar-codigo/$', 'puntodeventa.views.validar_codigo', name='validar_codigo'),
  url(r'^imprimir-ticket/$', 'puntodeventa.views.imprimir_ticket', name='imprimir_ticket'),
  url(r'^caja/$', 'puntodeventa.views.caja', name='caja'),
  url(r'^cobrar/$', 'puntodeventa.views.cobrar', name='cobrar'),
  url(r'^nodejs_ticket/$', 'puntodeventa.views.node_js_ticket', name='nodejs_ticket'),
  url(r'^sucursales/$', 'puntodeventa.views.sucursales', name='sucursales'),
  url(r'^cortez/$', 'puntodeventa.views.cortez', name='cortez'),
  url(r'^cortes/$', 'puntodeventa.views.cortes', name='cortes'),
  url(r'^corte-consulta/(.+)/$', 'puntodeventa.views.corte_consulta', name='corte_consulta'),
  url(r'^rasurado/$', 'puntodeventa.views.rasurado', name='rasurado'),
  url(r'^validar-supervisor/$', 'puntodeventa.views.validar_supervisor', name='validar_supervisor'),

  url(r'^administracion/', include(admin.site.urls)),
  url(r'media/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
  url(r'static/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
  url(r'^reset/$', 'puntodeventa.views.reset'),

)

