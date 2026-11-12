# OF_Cars · Django + MySQL

Este proyecto ahora está dentro de `HTML FO`. Los HTML originales se mantienen como maqueta; al ejecutar Django, la página principal y el panel usan las vistas dinámicas y los templates de `inventario/templates/inventario/`.

## Base de datos

Importa `base_datos/concesionario_orozco.sql` una sola vez si aún no creaste la base. Las tablas originales (`concesionario`, `administrador`, `marca`, `modelo`, `vehiculo`, `fotografia`) están mapeadas como `managed = False`, por lo que Django no las altera. La migración propia crea la tabla `venta`; las migraciones estándar de Django crean sus tablas de usuarios, permisos y sesiones.

La autenticación se hace con cuentas de Django, no con los valores de `administrador.contrasena_hash`. Crea el primer administrador con `createsuperuser`.

## Instalar y ejecutar en PowerShell

Abre `HTML FO` en Visual Studio Code y ejecuta:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Enciende MySQL y configura la conexión para la terminal:

```powershell
$env:DB_NAME = "concesionario_orozco"
$env:DB_USER = "root"
$env:DB_PASSWORD = "TU_CLAVE_MYSQL"
$env:DB_HOST = "127.0.0.1"
$env:DB_PORT = "3306"
```

Prepara las tablas adicionales de Django y la nueva tabla de ventas, crea la cuenta administradora y ejecuta el sitio:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abre <http://127.0.0.1:8000/>. El acceso está en `/acceso/`, el panel en `/panel/` y el administrador de cuentas de Django en `/admin/`.

## Funciones conectadas

- El catálogo consulta MySQL y aplica filtros de categoría, marca/modelo, precio, año, combustible y transmisión.
- Cada vehículo abre su ficha con fotografías y detalles.
- El personal autenticado publica y edita vehículos; las fotos se guardan en `media/vehiculos/` y sus rutas en la tabla `fotografia`.
- Al registrar una venta, Django crea el registro, calcula la comisión y cambia el vehículo a `Vendido`.
- El panel calcula ventas e ingresos mensuales/semanales con los registros de `venta`.

Para la previsualización de fotos en TypeScript, ejecuta `npm install` y `npm run build`. Ese paso solo compila la interfaz; las operaciones y persistencia las procesa Django/Python.
