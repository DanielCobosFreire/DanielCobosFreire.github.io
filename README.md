# CSi - CoFre Sistemas Informáticos (Semana 10 - Contenido dinámico con Jinja2)

## Novedades de esta semana
Sobre la base de Flask de la Semana 9, se incorporó contenido dinámico real
con Jinja2:

- **Variable simple**: `anio_actual` se inyecta en todas las plantillas
  mediante un `context_processor` en `app.py` y se muestra en
  `components/footer.html` con `{{ anio_actual }}`.
- **Diccionario/objeto estructurado**: `empresa_info` (nombre, slogan, año de
  fundación, misión, servicios destacados) se envía a `index.html` y se
  muestra con `{{ empresa.campo }}`.
- **Listas + `{% for %}`**: productos, clientes, proveedores y facturas siguen
  recorriéndose con bucles `for` (ya no se repite HTML a mano).
- **Condicionales `{% if %}/{% elif %}/{% else %}`**:
  - Productos: `Disponible` (stock > 0), `Agotado` (stock == 0) o `Servicio`
    (stock es `None`).
  - Clientes: `Cliente activo` / `Cliente inactivo`.
  - Facturación: `Pagada` (verde) / cualquier otro estado (amarillo).
- **Filtros de Jinja2**: `|upper` (empresa, categoría de producto, nombre de
  cliente, número de factura), `|lower` (contacto de proveedor), `|default`
  (footer) y `|format` (precios/totales, ya existente).
- **Componentes reutilizables**: `navbar` y `footer` se extrajeron a
  `templates/components/navbar.html` y `templates/components/footer.html`, e
  se incluyen en `base.html` con `{% include %}` en vez de repetirse en cada
  página.

## Estructura
```
csi-flask/
├── index.html            <- ORIGINAL sin cambios, es el que usa GitHub Pages
├── script.js              <- ORIGINAL sin cambios, referenciado por el index.html de arriba
├── app.py
├── requirements.txt
├── templates/              <- Solo para Flask (usa Jinja2, NO funciona en GitHub Pages)
│   ├── base.html
│   ├── index.html
│   ├── productos.html
│   ├── clientes.html
│   ├── proveedores.html
│   ├── facturacion.html
│   └── components/
│       ├── navbar.html
│       └── footer.html
└── static/                 <- Solo para Flask
    ├── css/style.css
    ├── js/script.js
    └── img/  (coloca aquí tus imágenes si usas alguna local)
```

**Importante:** GitHub Pages solo sirve archivos estáticos, no puede interpretar
`{% raw %}{{ url_for(...) }}{% endraw %}` ni las plantillas Jinja2. Por eso el `index.html` y `script.js`
de la raíz se mantienen exactamente como estaban (sin Jinja2) para que Pages los
siga publicando sin problema. La carpeta `templates/` es una versión aparte,
pensada para ejecutarse con `python app.py` en tu máquina.

## Probar localmente (opcional, requiere Python)
```
pip install flask
python app.py
```
Luego abre http://127.0.0.1:5000 y revisa /productos, /clientes, /proveedores y /facturacion.
Verifica en /productos que el "Teclado Mecánico RGB" aparezca como **Agotado**
(stock 0) y el resto como **Disponible** o **Servicio**.

## Subir a GitHub (flujo GUI, sin terminal)
1. No toques el `index.html` ni el `script.js` que ya tienes en la raíz de tu repo
   (son los que usa GitHub Pages) — déjalos tal cual.
2. Sube/reemplaza `app.py` y `requirements.txt` en la raíz del repositorio.
3. Dentro de `templates`, reemplaza `base.html`, `index.html`, `productos.html`,
   `clientes.html`, `proveedores.html` y `facturacion.html`.
4. Crea la carpeta `templates/components` y sube ahí `navbar.html` y `footer.html`.
5. `static/css/style.css`, `static/js/script.js` y `static/img` no cambiaron
   esta semana (déjalos como están si ya los subiste en la Semana 9).
6. Verifica que GitHub Pages siga mostrando la web con normalidad (usa el
   `index.html` de la raíz, no se ve afectado por estos cambios).
7. app.py + templates + static se ejecutan solo localmente con `python app.py`,
   tal como pide la tarea; no es necesario que Flask funcione desde Pages esta semana.
