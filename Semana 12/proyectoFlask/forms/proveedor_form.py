from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class ProveedorForm(FlaskForm):
    empresa = StringField('Nombre de la Empresa', validators=[
        DataRequired(message="El nombre de la empresa es obligatorio.")
    ])
    telefono = StringField('Teléfono', validators=[
        DataRequired(message="El teléfono es obligatorio."),
        Length(min=7, max=15, message="Ingrese un número de teléfono válido.")
    ])
    insumo = StringField('Insumo / Servicio', validators=[
        DataRequired(message="El insumo es obligatorio.")
    ])
    submit = SubmitField('Guardar Proveedor')