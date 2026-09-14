# CSi - CoFre Sistemas Informáticos (Semana 13 - Base de datos relacional)

## Novedades de esta semana
La aplicación evoluciona de SQLite (Semana 12) a una **base de datos
relacional real**: **PostgreSQL** (opción B de la consigna, usando
`psycopg2-binary`). El módulo de **Productos** implementa el flujo
completo pedido: **LISTAR (SELECT+JOIN) → AGREGAR (INSERT) → MODIFICAR
(UPDATE) → ELIMINAR (DELETE)**, todo contra PostgreSQL.

- **Conexión centralizada** en `conexion/conexion.py` (`obtener_conexion()`),
  expuesta a través de `conexion/__init__.py`. Las credenciales se leen de
  variables de entorno con valores por defecto para desarrollo local
  (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`).
- **Modelo relacional** con 4 tablas y una relación con `FOREIGN KEY`,
  guardado en `sql/esquema.sql`:
  - `proveedores(id_proveedor PK, nombre, telefono, correo)`
  - `productos(id_producto PK, nombre, categoria, precio, stock, id_proveedor FK → proveedores)`
  - `clientes(id_cliente PK, nombre, cedula, telefono, correo)` — tabla
    preparada, el módulo sigue usando una lista en memoria esta semana.
  - `facturas(id_factura PK, id_cliente FK → clientes, fecha, total)` —
    tabla preparada, igual que clientes.
- **`app.py`** ejecuta `sql/esquema.sql` al arrancar (`CREATE TABLE IF NOT
  EXISTS`, idempotente) y siembra proveedores/productos de ejemplo solo si
  las tablas están vacías.
- **Productos** ahora tiene un campo **Proveedor** (`SelectField`), cuyas
  opciones se cargan dinámicamente desde la tabla `proveedores` en cada
  request, antes de validar el formulario.
- **Listado con `JOIN`**: `productos.html` muestra el nombre real del
  proveedor de cada producto (`LEFT JOIN proveedores ... ON
  p.id_proveedor = pr.id_proveedor`), no solo su id.
- **INSERT y UPDATE parametrizados** (`%s`, nunca concatenación) en
  `formulario_producto`, con `WHERE id_producto = %s` en el UPDATE.
- **Nueva funcionalidad: Eliminar** (`DELETE FROM productos WHERE
  id_producto = %s`), con **confirmación visual** mediante un modal de
  Bootstrap antes de enviar el POST.
- **CSRF global**: se activó `CSRFProtect(app)` para que la nueva ruta de
  eliminación (que no usa una clase `FlaskForm`) también quede protegida,
  usando `{{ csrf_token() }}` directamente en la plantilla.
- Se comprobó **directamente en PostgreSQL** (vía `psql`) que INSERT,
  UPDATE y DELETE modifican realmente las filas, y que la restricción
  `FOREIGN KEY` rechaza un `id_proveedor` inexistente.
- Los módulos de **Clientes, Proveedores (catálogo propio) y Facturación**
  no cambiaron: siguen con listas de Python en memoria, "preparados" para
  su propia persistencia en un avance posterior.

## Estructura
```
csi-flask/
├── index.html            <- ORIGINAL sin cambios, es el que usa GitHub Pages
├── script.js              <- ORIGINAL sin cambios
├── app.py
├── requirements.txt
├── conexion/                <- NUEVO (Semana 13)
│   ├── __init__.py
│   └── conexion.py
├── sql/                     <- NUEVO (Semana 13)
│   └── esquema.sql
├── forms/
│   ├── __init__.py
│   ├── producto_form.py       (+ campo "proveedor")
│   ├── cliente_form.py
│   ├── proveedor_form.py
│   └── facturacion_form.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── productos.html            (JOIN + columna Proveedor + modal Eliminar)
│   ├── formulario_producto.html  (+ campo Proveedor)
│   ├── clientes.html
│   ├── formulario_cliente.html
│   ├── proveedores.html
│   ├── formulario_proveedor.html
│   ├── facturacion.html
│   ├── formulario_facturacion.html
│   └── components/
│       ├── navbar.html
│       └── footer.html
└── static/
    ├── css/style.css
    ├── js/script.js
    └── img/
```

**Nota:** la carpeta `data/` de la Semana 12 (SQLite) ya no se usa para
Productos; puede eliminarse del repositorio o dejarse como referencia
histórica, ya que esta semana la fuente real de datos es PostgreSQL.

**Importante:** GitHub Pages solo sirve archivos estáticos. Todo lo de
PostgreSQL (`conexion/`, `sql/`, la conexión en `app.py`) solo se ejecuta
localmente con `python app.py`.

## Configurar PostgreSQL localmente
1. Instala PostgreSQL (por ejemplo, con el instalador oficial en Windows,
   o `sudo apt install postgresql` en Linux).
2. Crea el usuario y la base de datos del proyecto (puedes ajustar el
   nombre/clave, pero entonces también ajusta las variables de entorno o
   los valores por defecto en `conexion/conexion.py`):
   ```sql
   CREATE USER csi_user WITH PASSWORD 'csi_password';
   CREATE DATABASE csi_ferreteria OWNER csi_user;
   GRANT ALL PRIVILEGES ON DATABASE csi_ferreteria TO csi_user;
   ```
3. (Opcional) Si prefieres crear el esquema tú mismo antes de correr Flask:
   ```
   psql -U csi_user -d csi_ferreteria -h localhost -f sql/esquema.sql
   ```
   No es obligatorio: `app.py` lo ejecuta automáticamente al arrancar.

## Probar localmente (requiere Python + PostgreSQL corriendo)
```
pip install -r requirements.txt
python app.py
```
Luego abre http://127.0.0.1:5000/productos y prueba el flujo completo:
1. **Listar**: deben aparecer los 5 productos de ejemplo, cada uno con su
   proveedor (o "Sin proveedor" para el servicio de mantenimiento).
2. **Agregar**: clic en "+ Nuevo Producto", completa el formulario
   (elige un proveedor o deja "Sin proveedor asignado") y guarda →
   aparece de inmediato en la tabla.
3. **Modificar**: clic en "Editar" sobre cualquier fila, cambia algún dato
   (incluido el proveedor) y guarda → se actualiza ese mismo registro.
4. **Eliminar**: clic en "Eliminar" → aparece un modal de confirmación;
   al aceptar, el producto desaparece de la tabla.
5. **Verificar en PostgreSQL directamente**, por ejemplo:
   ```
   psql -U csi_user -d csi_ferreteria -h localhost -c "SELECT * FROM productos;"
   ```
6. **Detén la aplicación (Ctrl+C) y vuelve a ejecutar `python app.py`.**
   Todos los cambios (altas, ediciones, bajas) deben seguir ahí — ya no
   se pierden al reiniciar, porque viven en PostgreSQL.

## Subir a GitHub (flujo GUI, sin terminal)
1. No toques el `index.html` ni el `script.js` de la raíz (los usa GitHub
   Pages) — déjalos tal cual.
2. Reemplaza `app.py` y `requirements.txt` en la raíz del repositorio.
3. Crea la carpeta `conexion` y sube ahí `__init__.py` y `conexion.py`.
4. Crea la carpeta `sql` y sube ahí `esquema.sql`.
5. Reemplaza `forms/producto_form.py` (ahora incluye el campo proveedor).
6. Dentro de `templates`, reemplaza `productos.html` y
   `formulario_producto.html`.
7. El resto (`base.html`, `components/`, `clientes.html`,
   `proveedores.html`, `facturacion.html` y sus formularios, `static/`)
   **no cambió** esta semana.
8. **No subas contraseñas reales** de PostgreSQL: `conexion/conexion.py`
   solo tiene valores de ejemplo para desarrollo local, pensados para
   sobreescribirse con variables de entorno.
9. Verifica que GitHub Pages siga mostrando la web con normalidad.
10. Ejecuta `python app.py` localmente con PostgreSQL corriendo, prueba
    el flujo completo (agregar, modificar, eliminar, reiniciar) y
    confirma los cambios directamente en la base de datos antes de dar
    por terminado el avance.

## Nota sobre cuántos archivos subir
Si tu plataforma limita la cantidad de archivos por entrega, para esta
semana **basta con subir los que realmente cambiaron o son nuevos**:
- `app.py`
- `conexion/__init__.py`
- `conexion/conexion.py`
- `sql/esquema.sql`
- `forms/producto_form.py`
- `templates/productos.html`
- `templates/formulario_producto.html`
- `requirements.txt`

Todo lo demás (el resto de formularios, plantillas, componentes y
estáticos) es idéntico a lo entregado en la Semana 12 y no necesita
volver a subirse.
