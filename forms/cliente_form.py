# forms/cliente_form.py
# Se conservan campos y validaciones de la Semana 11.
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ClienteForm(FlaskForm):
    nombre = StringField(
        "Nombre completo",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=100, message="Debe tener entre 3 y 100 caracteres."),
        ],
    )
    empresa = StringField(
        "Empresa",
        validators=[
            DataRequired(message="La empresa es obligatoria."),
            Length(min=2, max=120, message="Debe tener entre 2 y 120 caracteres."),
        ],
    )
    correo = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(message="El correo es obligatorio."),
            Email(message="Ingrese un correo electrónico válido."),
        ],
    )
    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio."),
            Length(min=7, max=15, message="Debe tener entre 7 y 15 caracteres."),
        ],
    )
    activo = BooleanField("Cliente activo", default=True)
    submit = SubmitField("Guardar Cliente")
