# forms/solicitud_form.py
# Módulo adicional inspirado en la mesa de ayuda de la página analizada.
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class SolicitudForm(FlaskForm):
    nombre = StringField(
        "Nombre del solicitante",
        validators=[DataRequired(message="El nombre es obligatorio."), Length(min=3, max=100)],
    )
    correo = StringField(
        "Correo electrónico",
        validators=[DataRequired(message="El correo es obligatorio."), Email(message="Ingrese un correo válido.")],
    )
    categoria = SelectField(
        "Categoría",
        choices=[
            ("Soporte Técnico", "Soporte Técnico"),
            ("Desarrollo Web", "Desarrollo Web"),
            ("Consultoría IT", "Consultoría IT"),
            ("Infraestructura", "Infraestructura"),
        ],
        validators=[DataRequired(message="Seleccione una categoría.")],
    )
    descripcion = TextAreaField(
        "Descripción",
        validators=[DataRequired(message="La descripción es obligatoria."), Length(min=10, max=800)],
    )
    estado = SelectField(
        "Estado",
        choices=[("Pendiente", "Pendiente"), ("En proceso", "En proceso"), ("Completada", "Completada")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Guardar Solicitud")
