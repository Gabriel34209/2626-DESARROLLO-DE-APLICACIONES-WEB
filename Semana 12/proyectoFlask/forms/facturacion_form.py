from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class FacturacionForm(FlaskForm):
    factura_no = StringField('Número de Factura', validators=[
        DataRequired(message="El número de factura es obligatorio.")
    ])
    cliente = StringField('Cliente', validators=[
        DataRequired(message="El cliente es obligatorio.")
    ])
    fecha = StringField('Fecha (AAAA-MM-DD)', validators=[
        DataRequired(message="La fecha es obligatoria.")
    ])
    total = FloatField('Monto Total ($)', validators=[
        DataRequired(message="El total es obligatorio."),
        NumberRange(min=0.01, message="El total debe ser mayor a 0.")
    ])
    submit = SubmitField('Guardar Factura')