#encoding:utf-8
from models import *
from forms import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group, Permission

admin.site.unregister(Site)
admin.site.unregister(Group)

class MyUserAdmin(UserAdmin):
    form = CambiarusuarioForm
    add_form = CrearusuarioForm

    list_display = ('usuario', 'perfil', 'sucursal')
    list_filter = ('sucursal','perfil' )
    
    fieldsets = (
                (None, {'fields': ('usuario', 'password')}),
                ('Perfil', {'fields': ('perfil','sucursal','codigo', 'supervisa')}),
                ('Permisos', {'fields': ('administrador', 'activo', 'user_permissions')}),
    )
    add_fieldsets = (
                    (None, {'classes': ('wide',), 'fields': ('usuario', 'password1', 'password2',)}),
    )
    search_fields = ('usuario',)
    ordering = ('usuario',)
    filter_horizontal = ('supervisa','user_permissions')
    exclude = ['is_superuser']

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'user_permissions':
            query = Permission.objects.filter(content_type__app_label="puntodeventa")
            kwargs['queryset'] = query
        return super(MyUserAdmin, self).formfield_for_manytomany(db_field, request=request, **kwargs)

class MenuAdmin(admin.ModelAdmin): 
    exclude = ['slugify']

class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nombre_comercial', 'menu_principal')
    search_fields = ('nombre', 'nombre_comercial')

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'alias', 'menu', 'precio','iva', 'principal', 'precio_dinamico')
    search_fields = ('nombre', 'alias')
    list_filter = ['menu']

class ProductosucursalAdmin(admin.ModelAdmin):
    list_display = ('producto', 'sucursal', 'inventario', 'merma')
    search_fields = ['producto__nombre']
    list_filter = ['sucursal']
    exclude = ('producto', 'sucursal')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('folio', 'sucursal', 'total', 'estatus', 'fecha','hora','corte')
    search_fields = ('folio','corte', 'fecha')
    list_filter = ['estatus']
    exclude = ('folio', 'sucursal','total','iva','corte','estatus')
    
    
        
admin.site.register(Usuario, MyUserAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Sucursal, SucursalAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Productosucursal, ProductosucursalAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Corte)




