from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("inventario", "0002_catalogo_original")]

    operations = [
        migrations.RunSQL(
            sql=(
                "ALTER TABLE vehiculo "
                "ADD COLUMN blindaje TINYINT(1) NULL, "
                "ADD COLUMN cilindraje INT NULL, "
                "ADD COLUMN condicion VARCHAR(20) NULL, "
                "ADD COLUMN tipo_precio VARCHAR(12) NULL, "
                "ADD COLUMN ultimo_digito_placa CHAR(1) NULL, "
                "ADD COLUMN asegurable TINYINT(1) NULL"
            ),
            reverse_sql=(
                "ALTER TABLE vehiculo "
                "DROP COLUMN blindaje, DROP COLUMN cilindraje, "
                "DROP COLUMN condicion, DROP COLUMN tipo_precio, "
                "DROP COLUMN ultimo_digito_placa, DROP COLUMN asegurable"
            ),
        ),
    ]
