# app.py
# CSi - CoFre Sistemas Informáticos
# Semana 9: configuración del proyecto con Flask y manejo de rutas.
# Semana 10: contenido dinámico con Jinja2 (variables, listas, diccionarios,
# estructuras repetitivas, condicionales y filtros).
# Semana 11: se incorporan formularios con Flask-WTF y WTForms, validación
# del lado del servidor, protección CSRF y una SECRET_KEY.
# Semana 12: persistencia local con SQLite para el módulo de Productos.
# Semana 13: la aplicación evoluciona de SQLite a una base de datos
# relacional real (PostgreSQL), con un modelo de varias tablas relacionadas
# mediante FOREIGN KEY (productos.id_proveedor -> proveedores.id_proveedor).
# El módulo de Productos implementa el flujo completo LISTAR (SELECT +
# JOIN), AGREGAR (INSERT), MODIFICAR (UPDATE) y ELIMINAR (DELETE) contra
# PostgreSQL. Clientes, proveedores (como catálogo propio) y facturación
# se mantienen con listas de Python en memoria, "preparados" para
# incorporar su propia persistencia en un avance posterior.

import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect

from conexion import obtener_conexion
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

# Semana 13: se activa CSRFProtect de forma global. Los formularios basados
# en FlaskForm (productos, clientes, proveedores, facturación) ya incluían
# su propio token vía form.hidden_tag(); esto además protege la nueva
# ruta de eliminación de productos, que envía un POST simple (sin una
# clase FlaskForm detrás) y usa {{ csrf_token() }} directamente en la plantilla.
csrf = CSRFProtect(app)


# =============================================================================
# Semana 13: inicialización del esquema relacional en PostgreSQL.
# Se ejecuta sql/esquema.sql (CREATE TABLE IF NOT EXISTS para las 4 tablas)
# y, si la tabla productos está vacía, se siembran algunos proveedores y
# productos de ejemplo para no perder los datos de demostración de
# semanas anteriores.
# =============================================================================
RUTA_ESQUEMA_SQL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sql', 'esquema.sql')


def inicializar_base_datos():
    """Crea las tablas del modelo relacional (si no existen) ejecutando
    sql/esquema.sql, y siembra datos de ejemplo solo la primera vez."""
    conn = obtener_conexion()
    with conn:
        with conn.cursor() as cur:
            with open(RUTA_ESQUEMA_SQL, 'r', encoding='utf-8') as archivo_sql:
                cur.execute(archivo_sql.read())
    _sembrar_datos_iniciales(conn)
    conn.close()


def _sembrar_datos_iniciales(conn):
    """Inserta proveedores y productos de ejemplo únicamente si las tablas
    todavía están vacías (para no duplicar datos en cada reinicio)."""
    with conn.cursor() as cur:
        cur.execute('SELECT COUNT(*) AS total FROM proveedores')
        if cur.fetchone()['total'] == 0:
            cur.execute(
                'INSERT INTO proveedores (nombre, telefono, correo) VALUES '
                '(%s, %s, %s), (%s, %s, %s), (%s, %s, %s)',
                (
                    'TecnoSuministros S.A.', '02-2345678', 'ventas@tecnosuministros.com',
                    'DistriSoft Ecuador', '02-3456789', 'contacto@distrisoft.ec',
                    'RedNet Cía. Ltda.', '02-4567890', 'info@rednet.ec',
                )
            )

        cur.execute('SELECT COUNT(*) AS total FROM productos')
        if cur.fetchone()['total'] == 0:
            cur.execute('SELECT id_proveedor, nombre FROM proveedores ORDER BY id_proveedor')
            proveedores = {fila['nombre']: fila['id_proveedor'] for fila in cur.fetchall()}

            productos_ejemplo = [
                ('Laptop HP 15"', 'Equipos', 650.00, 12, proveedores.get('TecnoSuministros S.A.')),
                ('Monitor LG 24"', 'Equipos', 180.00, 20, proveedores.get('TecnoSuministros S.A.')),
                ('Licencia Windows 11 Pro', 'Software', 199.00, 50, proveedores.get('DistriSoft Ecuador')),
                ('Teclado Mecánico RGB', 'Equipos', 55.00, 0, proveedores.get('TecnoSuministros S.A.')),
                ('Servicio de Mantenimiento IT', 'Servicios', 45.00, None, None),
            ]
            cur.executemany(
                'INSERT INTO productos (nombre, categoria, precio, stock, id_proveedor) '
                'VALUES (%s, %s, %s, %s, %s)',
                productos_ejemplo
            )
    conn.commit()


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
# Datos de ejemplo a nivel de módulo (listas mutables) para los módulos que
# TODAVÍA no tienen persistencia en base de datos. Productos ya no usa una
# lista ni SQLite: desde la Semana 13 se almacena en PostgreSQL (ver
# inicializar_base_datos, y las vistas 'productos' / 'formulario_producto'
# / 'eliminar_producto' más abajo).
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
    Semana 13: SELECT con JOIN hacia proveedores (clave foránea
    productos.id_proveedor -> proveedores.id_proveedor) para mostrar el
    nombre del proveedor de cada producto, no solo su id."""
    conn = obtener_conexion()
    with conn.cursor() as cur:
        cur.execute('''
            SELECT p.id_producto, p.nombre, p.categoria, p.precio, p.stock,
                   pr.id_proveedor AS id_proveedor,
                   pr.nombre AS proveedor_nombre
            FROM productos p
            LEFT JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
            ORDER BY p.id_producto
        ''')
        filas = cur.fetchall()
    conn.close()

    # RealDictCursor ya entrega cada fila como diccionario, listo para
    # que productos.html siga usando {{ producto.nombre }}, {{ producto.stock }},
    # {{ producto.proveedor_nombre }}, etc.
    return render_template('productos.html', productos=filas)


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
# Productos (Semana 13) usa el id_producto real de PostgreSQL, incluyendo
# la clave foránea hacia proveedores; clientes, proveedores y facturación
# siguen usando el índice de su lista en memoria, a la espera de
# incorporar su propia persistencia en un avance posterior.
# =============================================================================

def _obtener_choices_proveedores():
    """Consulta los proveedores existentes en PostgreSQL y arma la lista de
    choices para el SelectField 'proveedor' del formulario. Se incluye
    siempre la opción "Sin proveedor asignado" (id vacío -> NULL en la BD)."""
    conn = obtener_conexion()
    with conn.cursor() as cur:
        cur.execute('SELECT id_proveedor, nombre FROM proveedores ORDER BY nombre')
        filas = cur.fetchall()
    conn.close()
    choices = [('', 'Sin proveedor asignado')]
    choices += [(str(fila['id_proveedor']), fila['nombre']) for fila in filas]
    return choices


@app.route('/productos/nuevo', methods=['GET', 'POST'])
@app.route('/productos/editar/<int:producto_id>', methods=['GET', 'POST'])
def formulario_producto(producto_id=None):
    """Registro/edición de un producto. Reutiliza ProductoForm para ambos casos.

    Semana 13: el producto se busca, inserta o actualiza directamente en
    PostgreSQL, incluyendo la clave foránea hacia proveedores. 'producto_id'
    es la clave primaria real de la tabla 'productos' (columna id_producto)."""
    conn = obtener_conexion()

    if producto_id is not None:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM productos WHERE id_producto = %s', (producto_id,))
            fila = cur.fetchone()
        if fila is None:
            conn.close()
            flash('El producto solicitado no existe.', 'danger')
            return redirect(url_for('productos'))

        datos_iniciales = dict(fila)
        # El SelectField "proveedor" espera un string; la BD guarda un
        # entero (o NULL). '' representa "Sin proveedor asignado".
        datos_iniciales['proveedor'] = (
            str(datos_iniciales['id_proveedor']) if datos_iniciales['id_proveedor'] is not None else ''
        )
        form = ProductoForm(data=datos_iniciales)
    else:
        form = ProductoForm()

    # Las choices del proveedor se llenan dinámicamente con lo que exista
    # en la base de datos, ANTES de validar el formulario.
    form.proveedor.choices = _obtener_choices_proveedores()

    # form.validate_on_submit() se sigue evaluando ANTES de tocar la base
    # de datos; solo si los datos son válidos se ejecuta el INSERT o el UPDATE.
    if form.validate_on_submit():
        nombre = form.nombre.data
        categoria = form.categoria.data
        precio = form.precio.data
        stock = form.stock.data  # None si el campo se dejó en blanco (servicio)
        id_proveedor = int(form.proveedor.data) if form.proveedor.data else None

        with conn.cursor() as cur:
            if producto_id is not None:
                # UPDATE parametrizado (placeholders "%s", nunca concatenación
                # directa) con WHERE para modificar únicamente este producto.
                cur.execute(
                    '''UPDATE productos
                       SET nombre = %s, categoria = %s, precio = %s, stock = %s, id_proveedor = %s
                       WHERE id_producto = %s''',
                    (nombre, categoria, precio, stock, id_proveedor, producto_id)
                )
                flash('Producto actualizado correctamente.', 'success')
            else:
                # INSERT parametrizado
                cur.execute(
                    '''INSERT INTO productos (nombre, categoria, precio, stock, id_proveedor)
                       VALUES (%s, %s, %s, %s, %s)''',
                    (nombre, categoria, precio, stock, id_proveedor)
                )
                flash('Producto registrado correctamente.', 'success')

        conn.commit()
        conn.close()
        return redirect(url_for('productos'))

    conn.close()
    return render_template('formulario_producto.html', form=form, indice=producto_id)


@app.route('/productos/eliminar/<int:producto_id>', methods=['POST'])
def eliminar_producto(producto_id):
    """Elimina un único producto de PostgreSQL.
    Semana 13: DELETE parametrizado, siempre con WHERE por id_producto para
    no afectar el resto de la tabla; se pide confirmación visual en
    productos.html (modal de Bootstrap) antes de enviar este POST."""
    conn = obtener_conexion()
    with conn.cursor() as cur:
        cur.execute('SELECT nombre FROM productos WHERE id_producto = %s', (producto_id,))
        fila = cur.fetchone()
        if fila is None:
            conn.close()
            flash('El producto solicitado no existe o ya fue eliminado.', 'danger')
            return redirect(url_for('productos'))

        cur.execute('DELETE FROM productos WHERE id_producto = %s', (producto_id,))
    conn.commit()
    conn.close()

    flash(f'Producto "{fila["nombre"]}" eliminado correctamente.', 'success')
    return redirect(url_for('productos'))


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
