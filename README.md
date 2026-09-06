# CSi - CoFre Sistemas Informáticos (Semana 11 - Formularios con Flask-WTF)

## Novedades de esta semana
Sobre la base de Jinja2 de la Semana 10, se incorporaron formularios y
validación del lado del servidor con **Flask-WTF** y **WTForms**:

- **Carpeta `forms/`** con una clase de formulario por módulo, todas
  heredando de `FlaskForm`:
  `forms/producto_form.py`, `forms/cliente_form.py`,
  `forms/proveedor_form.py`, `forms/facturacion_form.py`.
- **SECRET_KEY** configurada en `app.py` (`app.config['SECRET_KEY']`),
  necesaria para que funcione la protección CSRF.
- **Validadores** usados según el tipo de dato: `DataRequired()`,
  `Length()`, `NumberRange()`, `Email()`, `Optional()` (stock de un
  "servicio", que puede ir en blanco) y `Regexp()` (formato de número de
  factura y de fecha).
- **Protección CSRF**: cada formulario incluye `{{ form.hidden_tag() }}`.
- **Rutas GET/POST** por módulo: `/productos/nuevo`, `/clientes/nuevo`,
  `/proveedores/nuevo`, `/facturacion/nueva`, y sus variantes
  `/editar/<indice>` para reutilizar el mismo formulario y la misma
  plantilla en el registro y en la edición.
- **`form.validate_on_submit()`**: los datos solo se procesan (se agregan
  o actualizan en la lista en memoria del módulo) cuando todas las
  validaciones pasan; si algo falla, se vuelve a mostrar el formulario con
  los mensajes de error debajo de cada campo.
- **Mensajes flash**: al guardar con éxito se muestra un aviso Bootstrap
  ("Producto registrado correctamente", etc.) en la parte superior del
  contenido, gracias a un bloque agregado en `base.html`.
- Cada módulo (productos, clientes, proveedores, facturación) tiene ahora
  un botón "+ Nuevo ..." y un botón "Editar" por fila/tarjeta.
- Los datos de ejemplo (antes definidos dentro de cada vista) ahora viven
  a nivel de módulo en `app.py`, para que lo que se registre o edite desde
  los formularios se conserve mientras el servidor siga corriendo. Sigue
  sin usarse base de datos.

## Estructura
```
csi-flask/
├── index.html            <- ORIGINAL sin cambios, es el que usa GitHub Pages
├── script.js              <- ORIGINAL sin cambios, referenciado por el index.html de arriba
├── app.py
├── requirements.txt
├── forms/                  <- NUEVO (Semana 11)
│   ├── __init__.py
│   ├── producto_form.py
│   ├── cliente_form.py
│   ├── proveedor_form.py
│   └── facturacion_form.py
├── templates/
│   ├── base.html            (ahora incluye el bloque de mensajes flash)
│   ├── index.html
│   ├── productos.html       (+ botón Nuevo/Editar)
│   ├── formulario_producto.html      <- NUEVO
│   ├── clientes.html        (+ botón Nuevo/Editar)
│   ├── formulario_cliente.html       <- NUEVO
│   ├── proveedores.html     (+ botón Nuevo/Editar)
│   ├── formulario_proveedor.html     <- NUEVO
│   ├── facturacion.html     (+ botón Nuevo/Editar)
│   ├── formulario_facturacion.html   <- NUEVO
│   └── components/
│       ├── navbar.html
│       └── footer.html
└── static/
    ├── css/style.css
    ├── js/script.js
    └── img/  (coloca aquí tus imágenes si usas alguna local)
```

**Importante:** GitHub Pages solo sirve archivos estáticos. El `index.html` y
`script.js` de la raíz se mantienen exactamente igual (sin Jinja2) para que
Pages los siga publicando sin problema. Todo lo de Flask-WTF/WTForms
(`forms/`, las nuevas plantillas de formulario, la SECRET_KEY) solo se
ejecuta localmente con `python app.py`.

## Probar localmente (requiere Python)
```
pip install -r requirements.txt
python app.py
```
Luego abre http://127.0.0.1:5000 y prueba, por ejemplo, en /productos:
1. Clic en "+ Nuevo Producto", dejar todo vacío y enviar → deben aparecer
   los mensajes de "obligatorio" debajo de cada campo, sin registrar nada.
2. Ingresar un precio negativo o un nombre muy corto → mensaje de
   validación correspondiente.
3. Completar correctamente (dejando "Stock" en blanco para un servicio, o
   con un número para un producto físico) → redirige al listado con un
   mensaje de éxito y el nuevo producto aparece en la tabla.
4. Clic en "Editar" sobre cualquier fila → el formulario aparece
   precargado con los datos existentes; al guardar, actualiza ese mismo
   registro (no crea uno nuevo).

Lo mismo aplica para /clientes, /proveedores y /facturacion (validaciones
de correo, teléfono, formato de número de factura F-001, etc.).

## Subir a GitHub (flujo GUI, sin terminal)
1. No toques el `index.html` ni el `script.js` que ya tienes en la raíz de
   tu repo (son los que usa GitHub Pages) — déjalos tal cual.
2. Sube/reemplaza `app.py` y `requirements.txt` en la raíz del repositorio.
3. Crea la carpeta `forms` en la raíz y sube ahí los 5 archivos `.py`
   (`__init__.py` y los 4 `*_form.py`).
4. Dentro de `templates`, reemplaza `base.html`, `productos.html`,
   `clientes.html`, `proveedores.html` y `facturacion.html`, y agrega las
   4 plantillas nuevas: `formulario_producto.html`,
   `formulario_cliente.html`, `formulario_proveedor.html`,
   `formulario_facturacion.html`.
5. `templates/components/`, `static/css/style.css`, `static/js/script.js`
   y `static/img` no cambiaron esta semana.
6. Verifica que GitHub Pages siga mostrando la web con normalidad (no se ve
   afectado por estos cambios).
7. Ejecuta `python app.py` localmente para comprobar que todas las rutas y
   formularios funcionan; no es necesario que Flask-WTF funcione desde
   Pages esta semana.
