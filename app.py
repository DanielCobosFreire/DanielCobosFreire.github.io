# app.py
# CSi - CoFre Sistemas Informáticos
# Semana 9: configuración del proyecto con Flask y manejo de rutas.
# Semana 10: se incorpora contenido dinámico con Jinja2 (variables, listas,
# diccionarios, estructuras repetitivas, condicionales y filtros), enviando
# los datos desde este archivo hacia las plantillas mediante render_template().
# Aún no se requiere conexión a una base de datos: los datos siguen siendo
# de ejemplo, definidos con listas y diccionarios de Python.

from datetime import datetime

from flask import Flask, render_template

app = Flask(__name__)


# =============================================================================
# Diccionario con información general de la empresa.
# Semana 10: ejemplo de "diccionario u objeto estructurado" enviado a una
# plantilla y consumido con {{ empresa.campo }} y con el filtro |upper.
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


@app.context_processor
def inyectar_variables_globales():
    """Variables simples disponibles en TODAS las plantillas (incluye base.html
    y sus componentes). Semana 10: ejemplo de "variable simple" enviada desde
    Flask y mostrada con {{ anio_actual }} en components/footer.html."""
    return {'anio_actual': datetime.now().year}


@app.route('/')
def index():
    """Página principal informativa (Quiénes somos, Servicios, Solicitudes, Contacto).
    Semana 10: se envía el diccionario 'empresa' para mostrar información
    dinámica de la compañía en la sección 'Quiénes Somos'."""
    return render_template('index.html', empresa=empresa_info)


@app.route('/productos')
def productos():
    """Módulo de Productos. Datos de ejemplo mientras no hay base de datos.
    Semana 10: se agrega un producto con stock=0 para poder evidenciar,
    dentro de la plantilla, el caso condicional 'Agotado'."""
    productos_data = [
        {'nombre': 'Laptop HP 15"', 'categoria': 'Equipos', 'precio': 650.00, 'stock': 12},
        {'nombre': 'Monitor LG 24"', 'categoria': 'Equipos', 'precio': 180.00, 'stock': 20},
        {'nombre': 'Licencia Windows 11 Pro', 'categoria': 'Software', 'precio': 199.00, 'stock': 50},
        {'nombre': 'Teclado Mecánico RGB', 'categoria': 'Equipos', 'precio': 55.00, 'stock': 0},
        {'nombre': 'Servicio de Mantenimiento IT', 'categoria': 'Servicios', 'precio': 45.00, 'stock': None},
    ]
    return render_template('productos.html', productos=productos_data)


@app.route('/clientes')
def clientes():
    """Módulo de Clientes. Datos de ejemplo mientras no hay base de datos."""
    clientes_data = [
        {'nombre': 'Juan Pérez', 'empresa': 'Ferretería El Tornillo',
         'correo': 'juan.perez@ejemplo.com', 'telefono': '098-123-4567', 'activo': True},
        {'nombre': 'María Torres', 'empresa': 'Panadería Dulce Trigo',
         'correo': 'maria.torres@ejemplo.com', 'telefono': '099-234-5678', 'activo': True},
        {'nombre': 'Carlos Mendoza', 'empresa': 'Colegio San Andrés',
         'correo': 'carlos.mendoza@ejemplo.com', 'telefono': '098-345-6789', 'activo': False},
    ]
    return render_template('clientes.html', clientes=clientes_data)


@app.route('/proveedores')
def proveedores():
    """Módulo de Proveedores. Datos de ejemplo mientras no hay base de datos."""
    proveedores_data = [
        {'nombre': 'TecnoSuministros S.A.', 'producto': 'Equipos de cómputo',
         'contacto': 'ventas@tecnosuministros.com'},
        {'nombre': 'DistriSoft Ecuador', 'producto': 'Licencias de software',
         'contacto': 'contacto@distrisoft.ec'},
        {'nombre': 'RedNet Cía. Ltda.', 'producto': 'Infraestructura de red',
         'contacto': 'info@rednet.ec'},
    ]
    return render_template('proveedores.html', proveedores=proveedores_data)


@app.route('/facturacion')
def facturacion():
    """Módulo de Facturación. Datos de ejemplo mientras no hay base de datos."""
    facturas_data = [
        {'numero': 'F-001', 'cliente': 'Juan Pérez', 'fecha': '2026-08-01',
         'total': 850.00, 'estado': 'Pagada'},
        {'numero': 'F-002', 'cliente': 'María Torres', 'fecha': '2026-08-05',
         'total': 199.00, 'estado': 'Pendiente'},
        {'numero': 'F-003', 'cliente': 'Carlos Mendoza', 'fecha': '2026-08-10',
         'total': 45.00, 'estado': 'Pagada'},
    ]
    return render_template('facturacion.html', facturas=facturas_data)


if __name__ == '__main__':
    app.run(debug=True)
