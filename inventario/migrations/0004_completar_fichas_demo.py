from django.db import migrations


# Valores de demostración para completar las publicaciones importadas.
# Los atributos específicos de cada unidad deben confirmarse con el concesionario.
DATOS = {
    1:  {"cilindraje": 1998, "condicion": "Usado", "tipo_precio": "Negociable", "blindaje": False, "ultimo_digito_placa": "4", "asegurable": True},
    2:  {"cilindraje": 1206, "condicion": "Usado", "tipo_precio": "Negociable", "blindaje": False, "ultimo_digito_placa": "7", "asegurable": True},
    3:  {"cilindraje": 1798, "condicion": "Usado", "tipo_precio": "Negociable", "blindaje": False, "ultimo_digito_placa": "2", "asegurable": True},
    4:  {"cilindraje": 1598, "condicion": "Usado", "tipo_precio": "Negociable", "blindaje": False, "ultimo_digito_placa": "9", "asegurable": True},
    5:  {"cilindraje": 1999, "condicion": "Usado", "tipo_precio": "Negociable", "blindaje": False, "ultimo_digito_placa": "1", "asegurable": True},
    6:  {"cilindraje": 1999, "condicion": "Usado", "tipo_precio": "Negociable", "blindaje": False, "ultimo_digito_placa": "6", "asegurable": True},
    7:  {"kilometraje": 245000, "combustible": "Gasolina", "transmision": "Manual", "color": "Blanco", "cilindraje": 4477, "condicion": "Usado", "tipo_precio": "Negociable", "blindaje": False, "ultimo_digito_placa": "3", "asegurable": True},
    8:  {"kilometraje": 198000, "combustible": "Gasolina", "transmision": "Manual", "color": "Beige", "cilindraje": 4477, "condicion": "Usado", "tipo_precio": "Negociable", "blindaje": False, "ultimo_digito_placa": "8", "asegurable": True},
    9:  {"kilometraje": 215000, "combustible": "Diésel", "transmision": "Manual", "color": "Blanco", "cilindraje": 2499, "condicion": "Usado", "tipo_precio": "Negociable", "blindaje": False, "ultimo_digito_placa": "5", "asegurable": True},
    10: {"kilometraje": 156000, "combustible": "Gasolina", "transmision": "Automática", "color": "Plata", "cilindraje": 3828, "condicion": "Usado", "tipo_precio": "Negociable", "blindaje": False, "ultimo_digito_placa": "0", "asegurable": True},
    11: {"kilometraje": 18000, "combustible": "Gasolina", "transmision": "Automática", "color": "Rojo", "cilindraje": 1998, "condicion": "Usado", "tipo_precio": "Negociable", "blindaje": False, "ultimo_digito_placa": "2", "asegurable": True},
    12: {"cilindraje": 1998, "condicion": "Usado", "tipo_precio": "Negociable", "blindaje": False, "ultimo_digito_placa": "6", "asegurable": True},
    13: {"kilometraje": 85000, "combustible": "Gasolina", "transmision": "Manual", "color": "Blanco", "cilindraje": 1591, "condicion": "Usado", "tipo_precio": "Negociable", "blindaje": False, "ultimo_digito_placa": "1", "asegurable": True},
    14: {"kilometraje": 0, "combustible": "Eléctrico", "transmision": "Automática", "color": "Gris", "cilindraje": None, "condicion": "Nuevo", "tipo_precio": "Fijo", "blindaje": False, "ultimo_digito_placa": "0", "asegurable": True},
    15: {"kilometraje": 128000, "combustible": "Gasolina", "transmision": "Manual", "color": "Gris", "cilindraje": 1598, "condicion": "Usado", "tipo_precio": "Negociable", "blindaje": False, "ultimo_digito_placa": "7", "asegurable": True},
    16: {"cilindraje": 2600, "condicion": "Nuevo", "tipo_precio": "Fijo", "blindaje": False, "ultimo_digito_placa": "4", "asegurable": True},
    17: {"cilindraje": 5193, "condicion": "Usado", "tipo_precio": "Negociable", "blindaje": False, "ultimo_digito_placa": "8", "asegurable": True},
    18: {"cilindraje": 1598, "condicion": "Usado", "tipo_precio": "Negociable", "blindaje": False, "ultimo_digito_placa": "3", "asegurable": True},
}


def completar(apps, schema_editor):
    for vehicle_id, values in DATOS.items():
        columnas = tuple(values)
        set_clause = ", ".join(f"{column} = %s" for column in columnas)
        with schema_editor.connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE vehiculo SET {set_clause} WHERE id_vehiculo = %s",
                [values[column] for column in columnas] + [vehicle_id],
            )


class Migration(migrations.Migration):
    dependencies = [("inventario", "0003_caracteristicas_vehiculo")]
    operations = [migrations.RunPython(completar, migrations.RunPython.noop)]
