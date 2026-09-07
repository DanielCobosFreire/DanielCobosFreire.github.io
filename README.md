# CSi - CoFre Sistemas Informáticos (Semana 12 - Persistencia con SQLite)

## Novedades de esta semana
Sobre la base de Flask-WTF de la Semana 11, se incorporó persistencia real
con **SQLite** para el módulo de **Productos**, siguiendo el flujo completo
pedido por la tarea: **Formulario → Validación → INSERT → SELECT → Jinja2**.

- **Base de datos** `data/ferreteria.db`, creada automáticamente al arrancar
  la aplicación (la carpeta `data/` se crea sola si no existe).
- **Conexión con `sqlite3`**: función `obtener_conexion()` en `app.py`, que
  abre una conexión nueva por operación (con `row_factory = sqlite3.Row`) y
  siempre se cierra con `conn.close()`.
- **Tabla `productos`** creada con `CREATE TABLE IF NOT EXISTS`, con clave
  primaria autoincremental (`id`) y columnas `nombre`, `categoria`,
  `precio`, `stock` (esta última puede ser `NULL` para representar un
  "Servicio", igual que en semanas anteriores).
- **Siembra inicial**: si la tabla está vacía (primera ejecución), se
  insertan los 5 productos de ejemplo de siempre; en ejecuciones
  posteriores no se duplican (se comprueba con `SELECT COUNT(*)`).
- **INSERT y UPDATE parametrizados** (`?`, nunca concatenación de strings)
  desde la vista `formulario_producto`, ejecutados únicamente cuando
  `form.validate_on_submit()` es verdadero. Se hace `conn.commit()`
  después de cada operación y `conn.close()` al final.
- **SELECT + `fetchall()`** en la vista `productos`, convertido a una lista
  de diccionarios y mostrado con el mismo bucle `{% for %}` de Jinja2 y los
  mismos estilos Bootstrap de siempre (Disponible / Agotado / Servicio).
- El enlace "Editar" de cada fila ahora usa el `id` real de la base de
  datos (`producto.id`) en vez de la posición en la lista.
- **Los demás módulos (clientes, proveedores, facturación) no cambiaron**:
  siguen usando listas de Python en memoria, tal como pide la consigna,
  listos para incorporar su propia persistencia en un avance posterior.
- Se comprobó que los productos registrados o editados **permanecen
  después de reiniciar la aplicación** (probado deteniendo y volviendo a
  levantar el proceso de Flask).

## Estructura
```
csi-flask/
├── index.html            <- ORIGINAL sin cambios, es el que usa GitHub Pages
├── script.js              <- ORIGINAL sin cambios, referenciado por el index.html de arriba
├── app.py
├── requirements.txt
├── data/                    <- NUEVO (Semana 12)
│   └── ferreteria.db          (se genera solo; incluida aquí ya sembrada)
├── forms/
│   ├── __init__.py
│   ├── producto_form.py
│   ├── cliente_form.py
│   ├── proveedor_form.py
│   └── facturacion_form.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── productos.html            (ahora lee de SQLite)
│   ├── formulario_producto.html  (INSERT/UPDATE en SQLite)
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

**Importante:** GitHub Pages solo sirve archivos estáticos. El `index.html`
y `script.js` de la raíz se mantienen exactamente igual (sin Jinja2). Todo
lo de SQLite (`data/`, la conexión en `app.py`) solo se ejecuta localmente
con `python app.py`.

## Probar localmente (requiere Python)
```
pip install -r requirements.txt
python app.py
```
Luego abre http://127.0.0.1:5000/productos y prueba:
1. Verifica que aparecen los 5 productos de ejemplo (Disponible / Agotado /
   Servicio según el stock).
2. Clic en "+ Nuevo Producto", completa el formulario y guarda → el nuevo
   producto aparece en la tabla.
3. Clic en "Editar" sobre cualquier fila, cambia algún dato y guarda → se
   actualiza ese mismo registro.
4. **Detén la aplicación (Ctrl+C) y vuelve a ejecutar `python app.py`.**
   Recarga `/productos`: los productos que registraste o editaste siguen
   ahí — ya no se pierden al reiniciar, porque viven en
   `data/ferreteria.db` y no en una lista de Python.
5. (Opcional) Abre `data/ferreteria.db` con "DB Browser for SQLite" para
   ver la tabla `productos` directamente.

## Subir a GitHub (flujo GUI, sin terminal)
1. No toques el `index.html` ni el `script.js` de la raíz (los usa GitHub
   Pages) — déjalos tal cual.
2. Reemplaza `app.py` en la raíz del repositorio.
3. Crea la carpeta `data` en la raíz y sube ahí `ferreteria.db` (o déjala
   vacía: la aplicación la crea sola la primera vez que corres
   `python app.py`, sembrando los 5 productos de ejemplo).
4. Dentro de `templates`, reemplaza `productos.html`.
5. `forms/`, el resto de `templates/` (`base.html`, `components/`,
   `clientes.html`, `proveedores.html`, `facturacion.html` y sus
   formularios) y `static/` **no cambiaron** esta semana — puedes dejarlos
   como ya los subiste en la Semana 11.
6. Verifica que GitHub Pages siga mostrando la web con normalidad (no se ve
   afectado por estos cambios).
7. Ejecuta `python app.py` localmente, registra un par de productos,
   reinicia la app y confirma que siguen apareciendo antes de dar por
   terminado el avance.

## Nota sobre cuántos archivos subir
Si tu plataforma limita la cantidad de archivos por entrega, para esta
semana **basta con subir los que realmente cambiaron**:
- `app.py`
- `templates/productos.html`
- `data/ferreteria.db` (o la carpeta `data/` vacía, si prefieres que Flask
  la genere sola al ejecutar)

Todo lo demás (formularios, resto de plantillas, componentes, estáticos)
es idéntico a lo entregado en la Semana 11 y no necesita volver a subirse.
