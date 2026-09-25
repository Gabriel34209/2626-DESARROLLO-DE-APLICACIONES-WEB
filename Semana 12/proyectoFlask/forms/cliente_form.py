from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre del Establecimiento', validators=[
        DataRequired(message="El nombre es obligatorio."),
        Length(min=3, max=100)
    ])
    contacto = StringField('Persona de Contacto', validators=[
        DataRequired(message="El contacto es obligatorio.")
    ])
    ciudad = StringField('Ciudad', validators=[
        DataRequired(message="La ciudad es obligatoria.")
    ])
    submit = SubmitField('Guardar Cliente')