# CSi - CoFre Sistemas Informáticos (Semana 9 - Flask)

## Estructura
```
csi-flask/
├── index.html          <- ORIGINAL sin cambios, es el que usa GitHub Pages
├── script.js            <- ORIGINAL sin cambios, referenciado por el index.html de arriba
├── app.py
├── templates/            <- Solo para Flask (usa Jinja2, NO funciona en GitHub Pages)
│   ├── base.html
│   ├── index.html
│   ├── productos.html
│   ├── clientes.html
│   ├── proveedores.html
│   └── facturacion.html
└── static/                <- Solo para Flask
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

## Subir a GitHub (flujo GUI, sin terminal)
1. No toques el `index.html` ni el `script.js` que ya tienes en la raíz de tu repo
   (son los que usa GitHub Pages) — déjalos tal cual.
2. Sube `app.py` a la raíz del repositorio.
3. Crea la carpeta `templates` y arrastra ahí los 6 archivos .html de esa carpeta.
4. Crea `static/css/style.css`, `static/js/script.js` y la carpeta `static/img`
   (agrega ahí tus imágenes si usas alguna local).
5. Verifica que GitHub Pages siga mostrando la web con normalidad (usa el
   `index.html` de la raíz, no se ve afectado por estos cambios).
6. app.py + templates + static se ejecutan solo localmente con `python app.py`,
   tal como pide la tarea; no es necesario que Flask funcione desde Pages esta semana.
