# app.py
# CSi - CoFre Sistemas Informáticos
# Proyecto Integrador - continuidad Semanas 9, 10, 11 y Avance Semana 12
# Semana 12: persistencia local con SQLite manteniendo Flask-WTF/WTForms,
# validaciones del servidor, métodos GET/POST, Jinja2, SECRET_KEY y CSRF.

import os
import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFError, CSRFProtect

from forms.cliente_form import ClienteForm
from forms.facturacion_form import FacturacionForm
from forms.producto_form import ProductoForm
from forms.proveedor_form import ProveedorForm
from forms.solicitud_form import SolicitudForm

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "csi.db"  # Se mantiene el nombre solicitado para el proyecto CSi.

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "csi-clave-secreta-semana12-cambiar-en-produccion"
)
app.config["WTF_CSRF_ENABLED"] = True

# Protección CSRF global: protege también los POST que no usan una clase FlaskForm,
# como los botones de eliminación.
csrf = CSRFProtect(app)

empresa_info = {
    "nombre": "CSi - CoFre Sistemas Informáticos",
    "marca": "CSi",
    "slogan": "Tecnología que resuelve, conecta y hace crecer.",
    "descripcion": (
        "Consultoría tecnológica, desarrollo web, soporte TI e infraestructura "
        "para empresas, profesionales y emprendimientos."
    ),
    "anio_fundacion": 2024,
}


def get_db_connection():
    """Abre una conexión SQLite y permite acceder a las columnas por nombre."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crea las tablas si todavía no existen. La BD nunca se elimina al iniciar."""
    conn = get_db_connection()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL CHECK (precio > 0),
            stock INTEGER CHECK (stock IS NULL OR stock >= 0)
        );

        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            empresa TEXT NOT NULL,
            correo TEXT NOT NULL,
            telefono TEXT NOT NULL,
            activo INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            producto TEXT NOT NULL,
            contacto TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL UNIQUE,
            cliente TEXT NOT NULL,
            fecha TEXT NOT NULL,
            total REAL NOT NULL CHECK (total > 0),
            estado TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS solicitudes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Pendiente',
            creada_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()
    conn.close()


def seed_db():
    """Carga ejemplos solo cuando una tabla está vacía; no borra registros existentes."""
    conn = get_db_connection()

    if conn.execute("SELECT COUNT(*) FROM productos").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
            [
                ('Laptop HP 15"', "Equipos", 650.00, 12),
                ('Monitor LG 24"', "Equipos", 180.00, 20),
                ("Licencia Windows 11 Pro", "Software", 199.00, 50),
                ("Servicio de Mantenimiento IT", "Servicios", 45.00, None),
            ],
        )

    if conn.execute("SELECT COUNT(*) FROM clientes").fetchone()[0] == 0:
        conn.executemany(
            """
            INSERT INTO clientes (nombre, empresa, correo, telefono, activo)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                ("Juan Pérez", "Comercial Andino", "juan.perez@ejemplo.com", "0981234567", 1),
                ("María Torres", "Emprendimiento Horizonte", "maria.torres@ejemplo.com", "0992345678", 1),
            ],
        )

    if conn.execute("SELECT COUNT(*) FROM proveedores").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO proveedores (nombre, producto, contacto) VALUES (?, ?, ?)",
            [
                ("TecnoSuministros S.A.", "Equipos de cómputo", "ventas@tecnosuministros.com"),
                ("DistriSoft Ecuador", "Licencias de software", "contacto@distrisoft.ec"),
            ],
        )

    if conn.execute("SELECT COUNT(*) FROM facturas").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO facturas (numero, cliente, fecha, total, estado) VALUES (?, ?, ?, ?, ?)",
            [
                ("F-001", "Juan Pérez", "2026-09-01", 850.00, "Pagada"),
                ("F-002", "María Torres", "2026-09-03", 199.00, "Pendiente"),
            ],
        )

    conn.commit()
    conn.close()


def fetch_all(query, params=()):
    """Ejecuta SELECT parametrizado y recupera los registros con fetchall()."""
    conn = get_db_connection()
    registros = conn.execute(query, params).fetchall()
    conn.close()
    return registros


def fetch_one(query, params=()):
    conn = get_db_connection()
    registro = conn.execute(query, params).fetchone()
    conn.close()
    return registro


init_db()
seed_db()


@app.context_processor
def inyectar_variables_globales():
    return {
        "anio_actual": datetime.now().year,
        "empresa": empresa_info,
    }


@app.errorhandler(CSRFError)
def manejar_error_csrf(error):
    flash(
        "No se pudo validar el formulario. Actualice la página e inténtelo nuevamente.",
        "danger",
    )
    return redirect(request.referrer or url_for("index"))


@app.route("/")
def index():
    servicios = fetch_all(
        "SELECT * FROM productos WHERE categoria = ? ORDER BY id DESC LIMIT 6",
        ("Servicios",),
    )
    stats = {
        "productos": fetch_one("SELECT COUNT(*) AS total FROM productos")["total"],
        "clientes": fetch_one("SELECT COUNT(*) AS total FROM clientes")["total"],
        "solicitudes": fetch_one("SELECT COUNT(*) AS total FROM solicitudes")["total"],
    }
    return render_template("index.html", servicios=servicios, stats=stats)


# =============================================================================
# PRODUCTOS - flujo mínimo exigido Semana 12:
# Formulario -> validate_on_submit() -> INSERT/UPDATE -> SELECT -> Jinja2
# =============================================================================
@app.route("/productos")
def productos():
    conn = get_db_connection()
    productos_db = conn.execute("SELECT * FROM productos ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("productos.html", productos=productos_db)


@app.route("/productos/nuevo", methods=["GET", "POST"])
@app.route("/productos/editar/<int:item_id>", methods=["GET", "POST"])
def formulario_producto(item_id=None):
    registro = fetch_one("SELECT * FROM productos WHERE id = ?", (item_id,)) if item_id else None

    if item_id and registro is None:
        flash("El producto solicitado no existe.", "danger")
        return redirect(url_for("productos"))

    form = ProductoForm(data=dict(registro) if registro and request.method == "GET" else None)

    if form.validate_on_submit():
        conn = get_db_connection()

        if item_id:
            conn.execute(
                """
                UPDATE productos
                SET nombre = ?, categoria = ?, precio = ?, stock = ?
                WHERE id = ?
                """,
                (
                    form.nombre.data.strip(),
                    form.categoria.data,
                    form.precio.data,
                    form.stock.data,
                    item_id,
                ),
            )
            flash("Producto actualizado correctamente.", "success")
        else:
            conn.execute(
                """
                INSERT INTO productos (nombre, categoria, precio, stock)
                VALUES (?, ?, ?, ?)
                """,
                (
                    form.nombre.data.strip(),
                    form.categoria.data,
                    form.precio.data,
                    form.stock.data,
                ),
            )
            flash("Producto registrado correctamente y almacenado en SQLite.", "success")

        conn.commit()
        conn.close()
        return redirect(url_for("productos"))

    return render_template("formulario_producto.html", form=form, item_id=item_id)


@app.post("/productos/eliminar/<int:item_id>")
def eliminar_producto(item_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM productos WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    flash("Producto eliminado correctamente.", "warning")
    return redirect(url_for("productos"))


# =============================================================================
# CLIENTES - persistencia SQLite adicional al mínimo solicitado.
# =============================================================================
@app.route("/clientes")
def clientes():
    clientes_db = fetch_all("SELECT * FROM clientes ORDER BY id DESC")
    return render_template("clientes.html", clientes=clientes_db)


@app.route("/clientes/nuevo", methods=["GET", "POST"])
@app.route("/clientes/editar/<int:item_id>", methods=["GET", "POST"])
def formulario_cliente(item_id=None):
    registro = fetch_one("SELECT * FROM clientes WHERE id = ?", (item_id,)) if item_id else None

    if item_id and registro is None:
        flash("El cliente solicitado no existe.", "danger")
        return redirect(url_for("clientes"))

    form = ClienteForm(data=dict(registro) if registro and request.method == "GET" else None)

    if form.validate_on_submit():
        valores = (
            form.nombre.data.strip(),
            form.empresa.data.strip(),
            form.correo.data.strip(),
            form.telefono.data.strip(),
            1 if form.activo.data else 0,
        )
        conn = get_db_connection()
        if item_id:
            conn.execute(
                """
                UPDATE clientes
                SET nombre = ?, empresa = ?, correo = ?, telefono = ?, activo = ?
                WHERE id = ?
                """,
                (*valores, item_id),
            )
            flash("Cliente actualizado correctamente.", "success")
        else:
            conn.execute(
                """
                INSERT INTO clientes (nombre, empresa, correo, telefono, activo)
                VALUES (?, ?, ?, ?, ?)
                """,
                valores,
            )
            flash("Cliente registrado correctamente.", "success")
        conn.commit()
        conn.close()
        return redirect(url_for("clientes"))

    return render_template("formulario_cliente.html", form=form, item_id=item_id)


@app.post("/clientes/eliminar/<int:item_id>")
def eliminar_cliente(item_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM clientes WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    flash("Cliente eliminado correctamente.", "warning")
    return redirect(url_for("clientes"))


# =============================================================================
# PROVEEDORES - persistencia SQLite adicional al mínimo solicitado.
# =============================================================================
@app.route("/proveedores")
def proveedores():
    proveedores_db = fetch_all("SELECT * FROM proveedores ORDER BY id DESC")
    return render_template("proveedores.html", proveedores=proveedores_db)


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@app.route("/proveedores/editar/<int:item_id>", methods=["GET", "POST"])
def formulario_proveedor(item_id=None):
    registro = fetch_one("SELECT * FROM proveedores WHERE id = ?", (item_id,)) if item_id else None

    if item_id and registro is None:
        flash("El proveedor solicitado no existe.", "danger")
        return redirect(url_for("proveedores"))

    form = ProveedorForm(data=dict(registro) if registro and request.method == "GET" else None)

    if form.validate_on_submit():
        valores = (
            form.nombre.data.strip(),
            form.producto.data.strip(),
            form.contacto.data.strip(),
        )
        conn = get_db_connection()
        if item_id:
            conn.execute(
                "UPDATE proveedores SET nombre = ?, producto = ?, contacto = ? WHERE id = ?",
                (*valores, item_id),
            )
            flash("Proveedor actualizado correctamente.", "success")
        else:
            conn.execute(
                "INSERT INTO proveedores (nombre, producto, contacto) VALUES (?, ?, ?)",
                valores,
            )
            flash("Proveedor registrado correctamente.", "success")
        conn.commit()
        conn.close()
        return redirect(url_for("proveedores"))

    return render_template("formulario_proveedor.html", form=form, item_id=item_id)


@app.post("/proveedores/eliminar/<int:item_id>")
def eliminar_proveedor(item_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM proveedores WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    flash("Proveedor eliminado correctamente.", "warning")
    return redirect(url_for("proveedores"))


# =============================================================================
# FACTURACIÓN - persistencia SQLite adicional al mínimo solicitado.
# =============================================================================
@app.route("/facturacion")
def facturacion():
    facturas_db = fetch_all("SELECT * FROM facturas ORDER BY fecha DESC, id DESC")
    return render_template("facturacion.html", facturas=facturas_db)


@app.route("/facturacion/nueva", methods=["GET", "POST"])
@app.route("/facturacion/editar/<int:item_id>", methods=["GET", "POST"])
def formulario_facturacion(item_id=None):
    registro = fetch_one("SELECT * FROM facturas WHERE id = ?", (item_id,)) if item_id else None

    if item_id and registro is None:
        flash("La factura solicitada no existe.", "danger")
        return redirect(url_for("facturacion"))

    form = FacturacionForm(data=dict(registro) if registro and request.method == "GET" else None)

    if form.validate_on_submit():
        valores = (
            form.numero.data.strip().upper(),
            form.cliente.data.strip(),
            form.fecha.data.strip(),
            form.total.data,
            form.estado.data,
        )
        conn = get_db_connection()
        try:
            if item_id:
                conn.execute(
                    """
                    UPDATE facturas
                    SET numero = ?, cliente = ?, fecha = ?, total = ?, estado = ?
                    WHERE id = ?
                    """,
                    (*valores, item_id),
                )
                flash("Factura actualizada correctamente.", "success")
            else:
                conn.execute(
                    """
                    INSERT INTO facturas (numero, cliente, fecha, total, estado)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    valores,
                )
                flash("Factura registrada correctamente.", "success")
            conn.commit()
        except sqlite3.IntegrityError:
            conn.rollback()
            flash("Ya existe una factura con ese número.", "danger")
            conn.close()
            return render_template("formulario_facturacion.html", form=form, item_id=item_id)

        conn.close()
        return redirect(url_for("facturacion"))

    return render_template("formulario_facturacion.html", form=form, item_id=item_id)


@app.post("/facturacion/eliminar/<int:item_id>")
def eliminar_factura(item_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM facturas WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    flash("Factura eliminada correctamente.", "warning")
    return redirect(url_for("facturacion"))


# =============================================================================
# SOLICITUDES - mejora tomada de la página analizada: mesa de ayuda persistente.
# =============================================================================
@app.route("/solicitudes")
def solicitudes():
    solicitudes_db = fetch_all("SELECT * FROM solicitudes ORDER BY id DESC")
    return render_template("solicitudes.html", solicitudes=solicitudes_db)


@app.route("/solicitudes/nueva", methods=["GET", "POST"])
@app.route("/solicitudes/editar/<int:item_id>", methods=["GET", "POST"])
def formulario_solicitud(item_id=None):
    registro = fetch_one("SELECT * FROM solicitudes WHERE id = ?", (item_id,)) if item_id else None

    if item_id and registro is None:
        flash("La solicitud indicada no existe.", "danger")
        return redirect(url_for("solicitudes"))

    form = SolicitudForm(data=dict(registro) if registro and request.method == "GET" else None)

    if form.validate_on_submit():
        valores = (
            form.nombre.data.strip(),
            form.correo.data.strip(),
            form.categoria.data,
            form.descripcion.data.strip(),
            form.estado.data,
        )
        conn = get_db_connection()
        if item_id:
            conn.execute(
                """
                UPDATE solicitudes
                SET nombre = ?, correo = ?, categoria = ?, descripcion = ?, estado = ?
                WHERE id = ?
                """,
                (*valores, item_id),
            )
            flash("Solicitud actualizada correctamente.", "success")
        else:
            conn.execute(
                """
                INSERT INTO solicitudes (nombre, correo, categoria, descripcion, estado)
                VALUES (?, ?, ?, ?, ?)
                """,
                valores,
            )
            flash("Solicitud registrada correctamente.", "success")
        conn.commit()
        conn.close()
        return redirect(url_for("solicitudes"))

    return render_template("formulario_solicitud.html", form=form, item_id=item_id)


@app.post("/solicitudes/eliminar/<int:item_id>")
def eliminar_solicitud(item_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM solicitudes WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    flash("Solicitud eliminada correctamente.", "warning")
    return redirect(url_for("solicitudes"))


if __name__ == "__main__":
    app.run(debug=True)
