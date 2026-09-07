# forms/producto_form.py
# Se conservan campos y validaciones de la Semana 11.
from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class ProductoForm(FlaskForm):
    nombre = StringField(
        "Nombre del producto",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=100, message="Debe tener entre 3 y 100 caracteres."),
        ],
    )
    categoria = SelectField(
        "Categoría",
        choices=[("Equipos", "Equipos"), ("Software", "Software"), ("Servicios", "Servicios")],
        validators=[DataRequired(message="Seleccione una categoría.")],
    )
    precio = FloatField(
        "Precio (USD)",
        validators=[
            DataRequired(message="El precio es obligatorio."),
            NumberRange(min=0.01, message="El precio debe ser mayor a 0."),
        ],
    )
    stock = IntegerField(
        "Stock (dejar en blanco si es un servicio)",
        validators=[Optional(), NumberRange(min=0, message="El stock no puede ser negativo.")],
    )
    submit = SubmitField("Guardar Producto")
