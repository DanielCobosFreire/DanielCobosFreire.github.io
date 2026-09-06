# forms/producto_form.py
# CSi - CoFre Sistemas Informáticos
# Semana 11: formulario del módulo de Productos con Flask-WTF y WTForms.
# La misma clase se reutiliza tanto para registrar un producto nuevo como
# para editar uno existente (ver app.py: vista formulario_producto).

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class ProductoForm(FlaskForm):
    """Formulario para registrar/editar un producto o servicio de CSi."""

    nombre = StringField(
        'Nombre del producto',
        validators=[DataRequired(message='El nombre es obligatorio.'),
                    Length(min=3, max=100, message='Debe tener entre 3 y 100 caracteres.')]
    )

    categoria = SelectField(
        'Categoría',
        choices=[
            ('Equipos', 'Equipos'),
            ('Software', 'Software'),
            ('Servicios', 'Servicios'),
        ],
        validators=[DataRequired(message='Seleccione una categoría.')]
    )

    precio = FloatField(
        'Precio (USD)',
        validators=[DataRequired(message='El precio es obligatorio.'),
                    NumberRange(min=0.01, message='El precio debe ser mayor a 0.')]
    )

    # Campo opcional: en blanco representa un producto tipo "Servicio"
    # (sin stock físico), tal como se maneja en productos.html (Semana 10).
    stock = IntegerField(
        'Stock (dejar en blanco si es un servicio)',
        validators=[Optional(),
                    NumberRange(min=0, message='El stock no puede ser negativo.')]
    )

    submit = SubmitField('Guardar Producto')
