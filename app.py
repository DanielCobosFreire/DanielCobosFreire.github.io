# app.py
# CSi - CoFre Sistemas Informáticos
# Semana 9: configuración del proyecto con Flask y manejo de rutas.
# Semana 10: contenido dinámico con Jinja2 (variables, listas, diccionarios,
# estructuras repetitivas, condicionales y filtros).
# Semana 11: se incorporan formularios con Flask-WTF y WTForms, validación
# del lado del servidor, protección CSRF y una SECRET_KEY.
# Semana 12: se incorpora persistencia real con SQLite para el módulo de
# Productos (flujo Formulario -> Validación -> INSERT -> SELECT -> Jinja2).
# Los demás módulos (clientes, proveedores, facturación) se mantienen con
# listas de Python en memoria, tal como quedaron en la Semana 11, listos
# para incorporar su propia persistencia en avances posteriores.

import os
import sqlite3
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, flash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)

# Semana 11: SECRET_KEY necesaria para que Flask-WTF pueda generar y
# validar el token CSRF de cada formulario. En un entorno real se leería
# desde una variable de entorno; aquí se deja un valor fijo para que el
# proyecto funcione de inmediato al ejecutarlo localmente.
app.config['SECRET_KEY'] = 'csi-clave-secreta-semana11-cambiar-en-produccion'


# =============================================================================
# Semana 12: configuración de la base de datos SQLite (data/ferreteria.db).
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'ferreteria.db')


def obtener_conexion():
    """Abre una nueva conexión a la base de datos SQLite.
    row_factory = sqlite3.Row permite acceder a las columnas por nombre
    (fila['nombre']) además de por posición, lo que facilita convertirlas
    a diccionarios para las plantillas Jinja2."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def inicializar_base_datos():
    """Crea la carpeta data/ y la tabla 'productos' si todavía no existen
    (CREATE TABLE IF NOT EXISTS), y siembra algunos productos de ejemplo
    únicamente la primera vez que se ejecuta la aplicación (tabla vacía),
    para no perder los datos de demostración de semanas anteriores."""
    os.makedirs(DATA_DIR, exist_ok=True)

    conn = obtener_conexion()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER
        )
    ''')
    conn.commit()

    total = conn.execute('SELECT COUNT(*) AS total FROM productos').fetchone()['total']
    if total == 0:
        productos_ejemplo = [
            ('Laptop HP 15"', 'Equipos', 650.00, 12),
            ('Monitor LG 24"', 'Equipos', 180.00, 20),
            ('Licencia Windows 11 Pro', 'Software', 199.00, 50),
            ('Teclado Mecánico RGB', 'Equipos', 55.00, 0),
            ('Servicio de Mantenimiento IT', 'Servicios', 45.00, None),
        ]
        conn.executemany(
            'INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)',
            productos_ejemplo
        )
        conn.commit()

    conn.close()


# Se inicializa la base de datos al arrancar la aplicación (una sola vez,
# de forma idempotente gracias a CREATE TABLE IF NOT EXISTS).
inicializar_base_datos()


# =============================================================================
# Diccionario con información general de la empresa (Semana 10).
# =============================================================================
empresa_info = {
    'nombre': 'CSi - CoFre Sistemas Informáticos',
    'slogan': 'Consultoría tecnológica, desarrollo web, soporte TI y transformación digital.',
    'anio_fundacion': 2024,
    'mision': (
        'Optimizar procesos de empresas y emprendedores mediante herramientas '
        'digitales modernas, seguras y escalables.'
    ),
    'servicios_destacados': ['Desarrollo Web', 'Consultoría IT', 'Soporte Técnico'],
}


# =============================================================================
# Semana 11: datos de ejemplo a nivel de módulo (listas mutables) para los
# módulos que TODAVÍA no tienen persistencia en base de datos. Productos ya
# no usa una lista: desde la Semana 12 se almacena en SQLite (ver más abajo
# 'inicializar_base_datos' y las vistas 'productos' / 'formulario_producto').
# =============================================================================
clientes_data = [
    {'nombre': 'Juan Pérez', 'empresa': 'Ferretería El Tornillo',
     'correo': 'juan.perez@ejemplo.com', 'telefono': '098-123-4567', 'activo': True},
    {'nombre': 'María Torres', 'empresa': 'Panadería Dulce Trigo',
     'correo': 'maria.torres@ejemplo.com', 'telefono': '099-234-5678', 'activo': True},
    {'nombre': 'Carlos Mendoza', 'empresa': 'Colegio San Andrés',
     'correo': 'carlos.mendoza@ejemplo.com', 'telefono': '098-345-6789', 'activo': False},
]

proveedores_data = [
    {'nombre': 'TecnoSuministros S.A.', 'producto': 'Equipos de cómputo',
     'contacto': 'ventas@tecnosuministros.com'},
    {'nombre': 'DistriSoft Ecuador', 'producto': 'Licencias de software',
     'contacto': 'contacto@distrisoft.ec'},
    {'nombre': 'RedNet Cía. Ltda.', 'producto': 'Infraestructura de red',
     'contacto': 'info@rednet.ec'},
]

facturas_data = [
    {'numero': 'F-001', 'cliente': 'Juan Pérez', 'fecha': '2026-08-01',
     'total': 850.00, 'estado': 'Pagada'},
    {'numero': 'F-002', 'cliente': 'María Torres', 'fecha': '2026-08-05',
     'total': 199.00, 'estado': 'Pendiente'},
    {'numero': 'F-003', 'cliente': 'Carlos Mendoza', 'fecha': '2026-08-10',
     'total': 45.00, 'estado': 'Pagada'},
]


@app.context_processor
def inyectar_variables_globales():
    """Variable simple 'anio_actual' disponible en todas las plantillas (Semana 10)."""
    return {'anio_actual': datetime.now().year}


# =============================================================================
# Página principal y módulos de listado (Semana 9-10, sin cambios de fondo)
# =============================================================================

@app.route('/')
def index():
    """Página principal informativa (Quiénes somos, Servicios, Solicitudes, Contacto)."""
    return render_template('index.html', empresa=empresa_info)


@app.route('/productos')
def productos():
    """Módulo de Productos: listado.
    Semana 12: los registros ya no vienen de una lista de Python, sino de
    una consulta SELECT a la base de datos SQLite (data/ferreteria.db)."""
    conn = obtener_conexion()
    filas = conn.execute('SELECT id, nombre, categoria, precio, stock FROM productos ORDER BY id').fetchall()
    conn.close()

    # Se convierte cada sqlite3.Row a un diccionario para que la plantilla
    # productos.html siga usando la misma sintaxis Jinja2 de siempre
    # ({{ producto.nombre }}, {{ producto.stock }}, etc.).
    productos_lista = [dict(fila) for fila in filas]
    return render_template('productos.html', productos=productos_lista)


@app.route('/clientes')
def clientes():
    """Módulo de Clientes: listado."""
    return render_template('clientes.html', clientes=clientes_data)


@app.route('/proveedores')
def proveedores():
    """Módulo de Proveedores: listado."""
    return render_template('proveedores.html', proveedores=proveedores_data)


@app.route('/facturacion')
def facturacion():
    """Módulo de Facturación: listado."""
    return render_template('facturacion.html', facturas=facturas_data)


# =============================================================================
# Formularios con Flask-WTF / WTForms (Semana 11).
# Cada vista acepta GET (mostrar el formulario, vacío o precargado) y POST
# (procesar y validar el envío). La misma vista y la misma plantilla sirven
# tanto para "nuevo" como para "editar".
# Productos (Semana 12) usa el id real de SQLite; clientes, proveedores y
# facturación siguen usando el índice de su lista en memoria, a la espera
# de incorporar su propia persistencia en un avance posterior.
# =============================================================================

@app.route('/productos/nuevo', methods=['GET', 'POST'])
@app.route('/productos/editar/<int:producto_id>', methods=['GET', 'POST'])
def formulario_producto(producto_id=None):
    """Registro/edición de un producto. Reutiliza ProductoForm para ambos casos.

    Semana 12: en lugar de una lista de Python, el producto se busca,
    inserta o actualiza directamente en SQLite. 'producto_id' es ahora la
    clave primaria real de la tabla 'productos' (columna id), no un simple
    índice de lista como en los demás módulos."""
    conn = obtener_conexion()

    if producto_id is not None:
        fila = conn.execute('SELECT * FROM productos WHERE id = ?', (producto_id,)).fetchone()
        if fila is None:
            conn.close()
            flash('El producto solicitado no existe.', 'danger')
            return redirect(url_for('productos'))
        form = ProductoForm(data=dict(fila))
    else:
        form = ProductoForm()

    # Semana 12: form.validate_on_submit() se sigue evaluando ANTES de
    # tocar la base de datos; solo si los datos son válidos se ejecuta
    # el INSERT o el UPDATE.
    if form.validate_on_submit():
        nombre = form.nombre.data
        categoria = form.categoria.data
        precio = form.precio.data
        stock = form.stock.data  # None si el campo se dejó en blanco (servicio)

        if producto_id is not None:
            # UPDATE parametrizado (placeholders "?", nunca concatenación directa)
            conn.execute(
                'UPDATE productos SET nombre = ?, categoria = ?, precio = ?, stock = ? WHERE id = ?',
                (nombre, categoria, precio, stock, producto_id)
            )
            flash('Producto actualizado correctamente.', 'success')
        else:
            # INSERT parametrizado
            conn.execute(
                'INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)',
                (nombre, categoria, precio, stock)
            )
            flash('Producto registrado correctamente.', 'success')

        conn.commit()
        conn.close()
        return redirect(url_for('productos'))

    conn.close()
    return render_template('formulario_producto.html', form=form, indice=producto_id)


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
@app.route('/clientes/editar/<int:indice>', methods=['GET', 'POST'])
def formulario_cliente(indice=None):
    """Registro/edición de un cliente. Reutiliza ClienteForm para ambos casos."""
    if indice is not None:
        if indice < 0 or indice >= len(clientes_data):
            flash('El cliente solicitado no existe.', 'danger')
            return redirect(url_for('clientes'))
        form = ClienteForm(data=clientes_data[indice])
    else:
        form = ClienteForm()

    if form.validate_on_submit():
        registro = {
            'nombre': form.nombre.data,
            'empresa': form.empresa.data,
            'correo': form.correo.data,
            'telefono': form.telefono.data,
            'activo': form.activo.data,
        }
        if indice is not None:
            clientes_data[indice] = registro
            flash('Cliente actualizado correctamente.', 'success')
        else:
            clientes_data.append(registro)
            flash('Cliente registrado correctamente.', 'success')
        return redirect(url_for('clientes'))

    return render_template('formulario_cliente.html', form=form, indice=indice)


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
@app.route('/proveedores/editar/<int:indice>', methods=['GET', 'POST'])
def formulario_proveedor(indice=None):
    """Registro/edición de un proveedor. Reutiliza ProveedorForm para ambos casos."""
    if indice is not None:
        if indice < 0 or indice >= len(proveedores_data):
            flash('El proveedor solicitado no existe.', 'danger')
            return redirect(url_for('proveedores'))
        form = ProveedorForm(data=proveedores_data[indice])
    else:
        form = ProveedorForm()

    if form.validate_on_submit():
        registro = {
            'nombre': form.nombre.data,
            'producto': form.producto.data,
            'contacto': form.contacto.data,
        }
        if indice is not None:
            proveedores_data[indice] = registro
            flash('Proveedor actualizado correctamente.', 'success')
        else:
            proveedores_data.append(registro)
            flash('Proveedor registrado correctamente.', 'success')
        return redirect(url_for('proveedores'))

    return render_template('formulario_proveedor.html', form=form, indice=indice)


@app.route('/facturacion/nueva', methods=['GET', 'POST'])
@app.route('/facturacion/editar/<int:indice>', methods=['GET', 'POST'])
def formulario_facturacion(indice=None):
    """Registro/edición de una factura. Reutiliza FacturacionForm para ambos casos."""
    if indice is not None:
        if indice < 0 or indice >= len(facturas_data):
            flash('La factura solicitada no existe.', 'danger')
            return redirect(url_for('facturacion'))
        form = FacturacionForm(data=facturas_data[indice])
    else:
        form = FacturacionForm()

    if form.validate_on_submit():
        registro = {
            'numero': form.numero.data,
            'cliente': form.cliente.data,
            'fecha': form.fecha.data,
            'total': form.total.data,
            'estado': form.estado.data,
        }
        if indice is not None:
            facturas_data[indice] = registro
            flash('Factura actualizada correctamente.', 'success')
        else:
            facturas_data.append(registro)
            flash('Factura registrada correctamente.', 'success')
        return redirect(url_for('facturacion'))

    return render_template('formulario_facturacion.html', form=form, indice=indice)


if __name__ == '__main__':
    app.run(debug=True)
