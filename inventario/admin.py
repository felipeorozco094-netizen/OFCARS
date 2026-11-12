from django.contrib import admin
from .models import Administrador, Concesionario, Fotografia, Marca, Modelo, Vehiculo, Venta

admin.site.site_header = "Administración OF_Cars"
admin.site.site_title = "OF_Cars"
admin.site.index_title = "Gestión del concesionario"
admin.site.register([Administrador, Concesionario, Fotografia, Marca, Modelo, Vehiculo, Venta])
