from django.db import models
from django.templatetags.static import static
from django.utils import timezone
from urllib.parse import urlparse


class Concesionario(models.Model):
    id_concesionario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    whatsapp = models.CharField(max_length=20, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    horario_atencion = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "concesionario"

    def __str__(self):
        return self.nombre


class Administrador(models.Model):
    id_administrador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    correo = models.CharField(max_length=150, unique=True)
    contrasena_hash = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "administrador"

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80, unique=True)

    class Meta:
        managed = False
        db_table = "marca"

    def __str__(self):
        return self.nombre


class Modelo(models.Model):
    id_modelo = models.AutoField(primary_key=True)
    marca = models.ForeignKey(Marca, models.DO_NOTHING, db_column="id_marca")
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "modelo"

    def __str__(self):
        return f"{self.marca} {self.nombre}"


class Vehiculo(models.Model):
    COMBUSTIBLES = [(v, v) for v in ("Gasolina", "Diésel", "Híbrido", "Eléctrico", "Gas")]
    TRANSMISIONES = [(v, v) for v in ("Manual", "Automática")]
    TIPOS = [(v, v) for v in ("Automóvil", "Camioneta", "SUV", "Pickup", "Camión")]
    ESTADOS = [(v, v) for v in ("Disponible", "Reservado", "Vendido")]
    CONDICIONES = [("Nuevo", "Nuevo"), ("Usado", "Usado")]
    TIPOS_PRECIO = [("Fijo", "Fijo"), ("Negociable", "Negociable")]

    id_vehiculo = models.AutoField(primary_key=True)
    modelo = models.ForeignKey(Modelo, models.DO_NOTHING, db_column="id_modelo")
    anio = models.IntegerField()
    precio = models.DecimalField(max_digits=14, decimal_places=2)
    kilometraje = models.IntegerField(default=0, blank=True, null=True)
    combustible = models.CharField(max_length=20, choices=COMBUSTIBLES, default="Gasolina", blank=True, null=True)
    transmision = models.CharField(max_length=20, choices=TRANSMISIONES, default="Manual", blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="Disponible", blank=True, null=True)
    fecha_publicacion = models.DateTimeField(blank=True, null=True)
    blindaje = models.BooleanField(blank=True, null=True)
    cilindraje = models.IntegerField(blank=True, null=True)
    condicion = models.CharField(max_length=20, choices=CONDICIONES, blank=True, null=True)
    tipo_precio = models.CharField(max_length=12, choices=TIPOS_PRECIO, blank=True, null=True)
    ultimo_digito_placa = models.CharField(max_length=1, blank=True, null=True)
    asegurable = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "vehiculo"
        indexes = [
            models.Index(fields=["precio"], name="idx_precio"),
            models.Index(fields=["anio"], name="idx_anio"),
            models.Index(fields=["tipo"], name="idx_tipo"),
        ]

    def __str__(self):
        return f"{self.modelo} {self.anio}"


class Fotografia(models.Model):
    id_foto = models.AutoField(primary_key=True)
    vehiculo = models.ForeignKey(Vehiculo, models.DO_NOTHING, db_column="id_vehiculo")
    url_imagen = models.CharField(max_length=500)
    es_principal = models.BooleanField(default=False, blank=True, null=True)
    orden = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "fotografia"
        ordering = ["-es_principal", "orden", "id_foto"]

    def __str__(self):
        return self.url_imagen

    @property
    def image_url(self):
        if self.url_imagen.startswith(("http://", "https://")):
            if urlparse(self.url_imagen).hostname == "cdn.concesionarioorozco.com":
                return static("inventario/imagenes/carredblack.png")
            return self.url_imagen
        if self.url_imagen.startswith("/"):
            return self.url_imagen
        if self.url_imagen.startswith("imagenes/"):
            return static(f"inventario/{self.url_imagen}")
        return static(f"inventario/imagenes/{self.url_imagen.rsplit('/', 1)[-1]}")


class Venta(models.Model):
    """Nueva tabla de movimientos; no altera las tablas heredadas de MySQL."""

    id_venta = models.BigAutoField(primary_key=True)
    vehiculo = models.ForeignKey(
        Vehiculo,
        models.PROTECT,
        db_column="id_vehiculo",
        related_name="ventas",
    )
    fecha_venta = models.DateTimeField(default=timezone.now)
    precio_venta = models.DecimalField(max_digits=14, decimal_places=2)
    porcentaje_comision = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=5,
    )
    comision = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        db_table = "venta"
        ordering = ["-fecha_venta"]

    def __str__(self):
        return f"Venta #{self.pk} · {self.vehiculo}"
