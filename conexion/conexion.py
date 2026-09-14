# conexion/conexion.py
# CSi - CoFre Sistemas Informáticos
# Semana 13: conexión centralizada con una base de datos relacional.
# Se eligió PostgreSQL (opción B de la consigna) usando psycopg2-binary.
# Todas las credenciales se leen de variables de entorno con valores por
# defecto pensados para desarrollo local; en un entorno real NUNCA se
# subiría una contraseña real al repositorio.

import os

import psycopg2
import psycopg2.extras

# Semana 13: parámetros de conexión. Se pueden sobreescribir con variables
# de entorno (por ejemplo en un archivo .env que NO se sube al repositorio)
# sin tener que tocar el código.
CONFIG_DB = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432'),
    'dbname': os.environ.get('DB_NAME', 'csi_ferreteria'),
    'user': os.environ.get('DB_USER', 'csi_user'),
    'password': os.environ.get('DB_PASSWORD', 'csi_password'),
}


def obtener_conexion():
    """Abre y devuelve una nueva conexión a PostgreSQL.

    Se usa cursor_factory=RealDictCursor para que cada fila se comporte
    como un diccionario (fila['nombre'] o fila.get('nombre')), lo que
    permite reutilizar exactamente la misma sintaxis Jinja2 de semanas
    anteriores en las plantillas ({{ producto.nombre }}, etc.).

    Quien llama a esta función es responsable de cerrar la conexión con
    conn.close() (y el cursor, si lo abrió explícitamente) una vez
    terminadas sus operaciones, tal como pide la consigna de la Semana 13.
    """
    return psycopg2.connect(
        host=CONFIG_DB['host'],
        port=CONFIG_DB['port'],
        dbname=CONFIG_DB['dbname'],
        user=CONFIG_DB['user'],
        password=CONFIG_DB['password'],
        cursor_factory=psycopg2.extras.RealDictCursor,
    )
