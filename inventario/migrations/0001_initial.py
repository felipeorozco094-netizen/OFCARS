from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Concesionario",
            fields=[
                ("id_concesionario", models.AutoField(primary_key=True, serialize=False)),
                ("nombre", models.CharField(max_length=150)),
                ("direccion", models.CharField(blank=True, max_length=255, null=True)),
                ("telefono", models.CharField(blank=True, max_length=20, null=True)),
                ("whatsapp", models.CharField(blank=True, max_length=20, null=True)),
                ("facebook", models.CharField(blank=True, max_length=255, null=True)),
                ("instagram", models.CharField(blank=True, max_length=255, null=True)),
                ("horario_atencion", models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={"db_table": "concesionario", "managed": False},
        ),
        migrations.CreateModel(
            name="Administrador",
            fields=[
                ("id_administrador", models.AutoField(primary_key=True, serialize=False)),
                ("nombre", models.CharField(max_length=150)),
                ("correo", models.CharField(max_length=150, unique=True)),
                ("contrasena_hash", models.CharField(max_length=255)),
                ("fecha_creacion", models.DateTimeField(blank=True, null=True)),
            ],
            options={"db_table": "administrador", "managed": False},
        ),
        migrations.CreateModel(
            name="Marca",
            fields=[
                ("id_marca", models.AutoField(primary_key=True, serialize=False)),
                ("nombre", models.CharField(max_length=80, unique=True)),
            ],
            options={"db_table": "marca", "managed": False},
        ),
        migrations.CreateModel(
            name="Modelo",
            fields=[
                ("id_modelo", models.AutoField(primary_key=True, serialize=False)),
                ("nombre", models.CharField(max_length=100)),
                ("marca", models.ForeignKey(db_column="id_marca", on_delete=django.db.models.deletion.DO_NOTHING, to="inventario.marca")),
            ],
            options={"db_table": "modelo", "managed": False},
        ),
        migrations.CreateModel(
            name="Vehiculo",
            fields=[
                ("id_vehiculo", models.AutoField(primary_key=True, serialize=False)),
                ("anio", models.IntegerField()),
                ("precio", models.DecimalField(decimal_places=2, max_digits=14)),
                ("kilometraje", models.IntegerField(blank=True, default=0, null=True)),
                ("combustible", models.CharField(blank=True, choices=[("Gasolina", "Gasolina"), ("Diésel", "Diésel"), ("Híbrido", "Híbrido"), ("Eléctrico", "Eléctrico"), ("Gas", "Gas")], default="Gasolina", max_length=20, null=True)),
                ("transmision", models.CharField(blank=True, choices=[("Manual", "Manual"), ("Automática", "Automática")], default="Manual", max_length=20, null=True)),
                ("color", models.CharField(blank=True, max_length=50, null=True)),
                ("tipo", models.CharField(choices=[("Automóvil", "Automóvil"), ("Camioneta", "Camioneta"), ("SUV", "SUV"), ("Pickup", "Pickup"), ("Camión", "Camión")], max_length=20)),
                ("descripcion", models.TextField(blank=True, null=True)),
                ("estado", models.CharField(blank=True, choices=[("Disponible", "Disponible"), ("Reservado", "Reservado"), ("Vendido", "Vendido")], default="Disponible", max_length=20, null=True)),
                ("fecha_publicacion", models.DateTimeField(blank=True, null=True)),
                ("modelo", models.ForeignKey(db_column="id_modelo", on_delete=django.db.models.deletion.DO_NOTHING, to="inventario.modelo")),
            ],
            options={
                "db_table": "vehiculo",
                "managed": False,
                "indexes": [
                    models.Index(fields=["precio"], name="idx_precio"),
                    models.Index(fields=["anio"], name="idx_anio"),
                    models.Index(fields=["tipo"], name="idx_tipo"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Fotografia",
            fields=[
                ("id_foto", models.AutoField(primary_key=True, serialize=False)),
                ("url_imagen", models.CharField(max_length=500)),
                ("es_principal", models.BooleanField(blank=True, default=False, null=True)),
                ("orden", models.IntegerField(blank=True, default=0, null=True)),
                ("vehiculo", models.ForeignKey(db_column="id_vehiculo", on_delete=django.db.models.deletion.DO_NOTHING, to="inventario.vehiculo")),
            ],
            options={"db_table": "fotografia", "managed": False, "ordering": ["orden", "id_foto"]},
        ),
        migrations.CreateModel(
            name="Venta",
            fields=[
                ("id_venta", models.BigAutoField(primary_key=True, serialize=False)),
                ("fecha_venta", models.DateTimeField(default=django.utils.timezone.now)),
                ("precio_venta", models.DecimalField(decimal_places=2, max_digits=14)),
                ("porcentaje_comision", models.DecimalField(decimal_places=2, default=5, max_digits=5)),
                ("comision", models.DecimalField(decimal_places=2, max_digits=14)),
                ("vehiculo", models.ForeignKey(db_column="id_vehiculo", on_delete=django.db.models.deletion.PROTECT, related_name="ventas", to="inventario.vehiculo")),
            ],
            options={"db_table": "venta", "ordering": ["-fecha_venta"]},
        ),
    ]
