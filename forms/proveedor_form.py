# forms/proveedor_form.py
# Se conservan campos y validaciones de la Semana 11.
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ProveedorForm(FlaskForm):
    nombre = StringField(
        "Nombre del proveedor",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=120, message="Debe tener entre 3 y 120 caracteres."),
        ],
    )
    producto = StringField(
        "Producto / Servicio que ofrece",
        validators=[
            DataRequired(message="Este campo es obligatorio."),
            Length(min=3, max=120, message="Debe tener entre 3 y 120 caracteres."),
        ],
    )
    contacto = StringField(
        "Correo de contacto",
        validators=[
            DataRequired(message="El correo de contacto es obligatorio."),
            Email(message="Ingrese un correo electrónico válido."),
        ],
    )
    submit = SubmitField("Guardar Proveedor")
