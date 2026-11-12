from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from inventario import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.inicio, name="inicio"),
    path("vehiculo/<int:vehiculo_id>/", views.detalle_vehiculo, name="detalle_vehiculo"),
    path("acceso/", views.acceso, name="acceso"),
    path("salir/", views.salir, name="salir"),
    path("panel/", views.panel, name="panel"),
    path("panel/vehiculos/", views.inventario_admin, name="inventario_admin"),
    path("panel/vehiculos/nuevo/", views.crear_vehiculo, name="crear_vehiculo"),
    path("panel/vehiculos/<int:vehiculo_id>/editar/", views.editar_vehiculo, name="editar_vehiculo"),
    path("panel/ventas/nueva/", views.registrar_venta, name="registrar_venta"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
