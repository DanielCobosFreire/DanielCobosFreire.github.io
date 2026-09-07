# Evidencia técnica - Semana 12

## Flujo mínimo de productos

1. **Formulario:** `forms/producto_form.py`
2. **Validación:** `form.validate_on_submit()` en `app.py`
3. **INSERT:** `INSERT INTO productos ... VALUES (?, ?, ?, ?)`
4. **Persistencia:** `conn.commit()` en `data/csi.db`
5. **SELECT:** ruta `/productos`
6. **Recuperación:** `.fetchall()`
7. **Jinja2:** `templates/productos.html`
8. **Tabla Bootstrap:** tabla responsive con ciclo `{% for p in productos %}`

## CSRF

- `SECRET_KEY` configurada en Flask.
- `CSRFProtect(app)` protege globalmente solicitudes POST.
- Los formularios Flask-WTF incluyen `form.hidden_tag()`.
- Los formularios de eliminación incluyen `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`.

## Persistencia

`data/csi.db` no se elimina al ejecutar la aplicación. `init_db()` utiliza `CREATE TABLE IF NOT EXISTS`, por lo que los registros permanecen después de detener y volver a iniciar Flask.
