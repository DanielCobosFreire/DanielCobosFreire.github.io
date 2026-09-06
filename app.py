# app.py
# CSi - CoFre Sistemas Informáticos
# Semana 9: configuración del proyecto con Flask y manejo de rutas.
# Semana 10: contenido dinámico con Jinja2 (variables, listas, diccionarios,
# estructuras repetitivas, condicionales y filtros).
# Semana 11: se incorporan formularios con Flask-WTF y WTForms, validación
# del lado del servidor, protección CSRF y una SECRET_KEY. Los datos siguen
# siendo estructuras de Python en memoria (sin base de datos todavía); ahora
# viven a nivel de módulo para que los registros creados/editados desde los
# formularios persistan mientras la aplicación esté corriendo.

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
# Semana 11: los datos de ejemplo pasan a vivir a nivel de módulo (listas
# mutables) en lugar de crearse dentro de cada función de vista. Así, los
# registros que se agreguen o editen desde los formularios se conservan
# mientras el servidor de desarrollo siga corriendo. Sigue sin usarse una
# base de datos: es el mismo tipo de estructura de Python de semanas
# anteriores, solo que ahora es compartida entre las vistas de listado y
# las vistas de formulario.
# =============================================================================
productos_data = [
    {'nombre': 'Laptop HP 15"', 'categoria': 'Equipos', 'precio': 650.00, 'stock': 12},
    {'nombre': 'Monitor LG 24"', 'categoria': 'Equipos', 'precio': 180.00, 'stock': 20},
    {'nombre': 'Licencia Windows 11 Pro', 'categoria': 'Software', 'precio': 199.00, 'stock': 50},
    {'nombre': 'Teclado Mecánico RGB', 'categoria': 'Equipos', 'precio': 55.00, 'stock': 0},
    {'nombre': 'Servicio de Mantenimiento IT', 'categoria': 'Servicios', 'precio': 45.00, 'stock': None},
]

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
    """Módulo de Productos: listado."""
    return render_template('productos.html', productos=productos_data)


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
# Semana 11: formularios con Flask-WTF / WTForms.
# Cada vista acepta GET (mostrar el formulario, vacío o precargado) y POST
# (procesar y validar el envío). La misma vista y la misma plantilla sirven
# tanto para "nuevo" como para "editar", pasando opcionalmente un índice de
# la lista en memoria (equivalente temporal a un id, hasta que se incorpore
# una base de datos en un avance posterior).
# =============================================================================

@app.route('/productos/nuevo', methods=['GET', 'POST'])
@app.route('/productos/editar/<int:indice>', methods=['GET', 'POST'])
def formulario_producto(indice=None):
    """Registro/edición de un producto. Reutiliza ProductoForm para ambos casos."""
    if indice is not None:
        if indice < 0 or indice >= len(productos_data):
            flash('El producto solicitado no existe.', 'danger')
            return redirect(url_for('productos'))
        form = ProductoForm(data=productos_data[indice])
    else:
        form = ProductoForm()

    if form.validate_on_submit():
        registro = {
            'nombre': form.nombre.data,
            'categoria': form.categoria.data,
            'precio': form.precio.data,
            'stock': form.stock.data,  # None si el campo se dejó en blanco (servicio)
        }
        if indice is not None:
            productos_data[indice] = registro
            flash('Producto actualizado correctamente.', 'success')
        else:
            productos_data.append(registro)
            flash('Producto registrado correctamente.', 'success')
        return redirect(url_for('productos'))

    return render_template('formulario_producto.html', form=form, indice=indice)


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
