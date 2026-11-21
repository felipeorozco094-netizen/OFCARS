from decimal import Decimal

from django.db import migrations
from django.utils import timezone


VEHICULOS_INICIALES = (
    {
        "marca": "Toyota",
        "modelo": "Land Cruiser Serie 80",
        "anio": 1996,
        "precio": "40000000.00",
        "tipo": "Camioneta",
        "descripcion": "Toyota Land Cruiser Serie 80 modelo 1996.",
        "foto": "imagenes/burbuja.jpg",
    },
    {
        "marca": "Toyota",
        "modelo": "Land Cruiser Serie 70",
        "anio": 1999,
        "precio": "120000000.00",
        "tipo": "Camioneta",
        "descripcion": "Toyota Land Cruiser Serie 70 modelo 1999.",
        "foto": "imagenes/machito.jpg",
    },
    {
        "marca": "Chevrolet",
        "modelo": "D-Max Estacas",
        "anio": 2012,
        "precio": "62000000.00",
        "tipo": "Pickup",
        "descripcion": "Chevrolet D-Max modelo 2012 con carrocería de estacas.",
        "foto": "imagenes/dmax estacas.webp",
    },
    {
        "marca": "Mitsubishi",
        "modelo": "Montero Wagon",
        "anio": 2008,
        "precio": "65000000.00",
        "tipo": "SUV",
        "descripcion": "Mitsubishi Montero Wagon, cuatro puertas, modelo 2008.",
        "foto": "imagenes/montero.jpg",
    },
    {
        "marca": "Mazda",
        "modelo": "CX-30",
        "anio": 2024,
        "precio": "105000000.00",
        "tipo": "SUV",
        "descripcion": "Mazda CX-30 modelo 2024.",
        "foto": "imagenes/cx 30.webp",
    },
    {
        "marca": "Mazda",
        "modelo": "3 Grand Touring",
        "anio": 2023,
        "precio": "78000000.00",
        "tipo": "Automóvil",
        "descripcion": "Mazda 3 Grand Touring modelo 2023.",
        "foto": "imagenes/mazda 3.webp",
    },
    {
        "marca": "Kia",
        "modelo": "Cerato Pro",
        "anio": 2016,
        "precio": "45000000.00",
        "tipo": "Automóvil",
        "descripcion": "Kia Cerato Pro modelo 2016.",
        "foto": "imagenes/ceratopro.webp",
    },
    {
        "marca": "Tesla",
        "modelo": "Model 3",
        "anio": 2026,
        "precio": "120000000.00",
        "tipo": "Automóvil",
        "descripcion": "Tesla Model 3 modelo 2026.",
        "foto": "imagenes/model 3.jpg",
    },
    {
        "marca": "Chevrolet",
        "modelo": "Aveo Emotion",
        "anio": 2010,
        "precio": "36000000.00",
        "tipo": "Automóvil",
        "descripcion": "Chevrolet Aveo Emotion, full equipo, modelo 2010.",
        "foto": "imagenes/aveo emotion.webp",
    },
)


def cargar_catalogo(apps, schema_editor):
    alias = schema_editor.connection.alias
    ConcesionarioMarca = apps.get_model("inventario", "Marca")
    ConcesionarioModelo = apps.get_model("inventario", "Modelo")
    Vehiculo = apps.get_model("inventario", "Vehiculo")
    Fotografia = apps.get_model("inventario", "Fotografia")

    for datos in VEHICULOS_INICIALES:
        marca, _ = ConcesionarioMarca.objects.using(alias).get_or_create(
            nombre=datos["marca"]
        )
        modelo, _ = ConcesionarioModelo.objects.using(alias).get_or_create(
            marca_id=marca.pk,
            nombre=datos["modelo"],
        )
        vehiculo, _ = Vehiculo.objects.using(alias).get_or_create(
            modelo_id=modelo.pk,
            anio=datos["anio"],
            precio=Decimal(datos["precio"]),
            tipo=datos["tipo"],
            defaults={
                "kilometraje": None,
                "combustible": None,
                "transmision": None,
                "color": None,
                "descripcion": datos["descripcion"],
                "estado": "Disponible",
                "fecha_publicacion": timezone.now(),
            },
        )
        Fotografia.objects.using(alias).get_or_create(
            vehiculo_id=vehiculo.pk,
            url_imagen=datos["foto"],
            defaults={"es_principal": True, "orden": 0},
        )


class Migration(migrations.Migration):
    dependencies = [("inventario", "0001_initial")]

    operations = [migrations.RunPython(cargar_catalogo, migrations.RunPython.noop)]
