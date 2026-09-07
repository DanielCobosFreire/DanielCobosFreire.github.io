# CSi - CoFre Sistemas Informáticos
## Proyecto Integrador U3 - Avance Semana 12/16

Este repositorio continúa el proyecto desarrollado en las semanas anteriores. En la Semana 11 se incorporaron Flask-WTF, WTForms, validación del lado del servidor, métodos GET/POST, `form.validate_on_submit()`, `SECRET_KEY` y tokens CSRF. En este avance se integra persistencia local mediante SQLite sin reemplazar los formularios existentes.

## Cambios de Semana 12

- Persistencia real con SQLite usando el módulo estándar `sqlite3`.
- Base de datos local: `data/csi.db`.
- `sqlite3.connect()` en `get_db_connection()`.
- Tablas creadas con `CREATE TABLE IF NOT EXISTS`.
- Claves primarias `INTEGER PRIMARY KEY AUTOINCREMENT`.
- Flujo completo de productos: Flask-WTF → `validate_on_submit()` → `INSERT` → `commit()` → `SELECT` → `fetchall()` → Jinja2 → tabla Bootstrap.
- Consultas SQL parametrizadas mediante `?`.
- Conexiones cerradas con `conn.close()`.
- Persistencia también para clientes, proveedores, facturación y solicitudes.
- Protección CSRF global mediante `CSRFProtect(app)`.
- Formularios Flask-WTF siguen utilizando `{{ form.hidden_tag() }}`.
- Los formularios POST de eliminación incluyen `csrf_token` explícito.
- Se mantienen `base.html`, componentes reutilizables `navbar.html` y `footer.html`, `url_for()`, y recursos en `static/`.
- Se incorpora una mesa de ayuda/solicitudes como mejora funcional inspirada en el proyecto analizado.
- Se mejora la interfaz conservando la identidad visual de CSi.

> **Nota sobre el nombre de la base:** la guía académica usa `ferreteria.db` como nombre de referencia. En este proyecto se conserva deliberadamente `csi.db` para mantener la identidad y continuidad del emprendimiento CSi, según la decisión del proyecto.

## Estructura

```text
Semana_011/
├── app.py
├── requirements.txt
├── index.html                 # versión estática compatible con GitHub Pages
├── script.js                  # JS de la versión estática
├── data/
│   └── csi.db
├── forms/
│   ├── __init__.py
│   ├── producto_form.py
│   ├── cliente_form.py
│   ├── proveedor_form.py
│   ├── facturacion_form.py
│   └── solicitud_form.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── productos.html
│   ├── formulario_producto.html
│   ├── clientes.html
│   ├── formulario_cliente.html
│   ├── proveedores.html
│   ├── formulario_proveedor.html
│   ├── facturacion.html
│   ├── formulario_facturacion.html
│   ├── solicitudes.html
│   ├── formulario_solicitud.html
│   ├── _form_macros.html
│   └── components/
│       ├── navbar.html
│       └── footer.html
└── static/
    ├── css/style.css
    ├── js/script.js
    └── img/
```

## Ejecutar localmente

```bash
python -m venv .venv
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Windows:

```bat
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abrir: `http://127.0.0.1:5000`

## Prueba de persistencia para la evidencia

1. Ir a `/productos`.
2. Registrar al menos dos productos válidos.
3. Confirmar que aparecen en la tabla.
4. Detener Flask (`Ctrl+C`).
5. Ejecutar nuevamente `python app.py`.
6. Volver a `/productos`.
7. Verificar que los productos siguen almacenados.

La aplicación no elimina ni recrea `csi.db`; `CREATE TABLE IF NOT EXISTS` solo garantiza que las tablas existan.

## Qué demostrar al docente

En `app.py` se pueden localizar directamente:

- `sqlite3.connect(DB_PATH)`
- `CREATE TABLE IF NOT EXISTS productos`
- `form.validate_on_submit()`
- `INSERT INTO productos ... VALUES (?, ?, ?, ?)`
- `conn.commit()`
- `conn.close()`
- `SELECT * FROM productos ...`
- `.fetchall()`
- `render_template("productos.html", productos=productos_db)`
- `CSRFProtect(app)`

En `templates/productos.html` se evidencia el ciclo `{% for p in productos %}` y la tabla Bootstrap.

## GitHub Pages

GitHub Pages solo ejecuta el `index.html` estático de la raíz. Flask, Flask-WTF y SQLite deben demostrarse localmente. La página estática continúa disponible como evidencia visual y usa `localStorage` para sus solicitudes; esto es independiente de `csi.db`.
