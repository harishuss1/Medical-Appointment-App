from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, PasswordField, RadioField
from wtforms.validators import DataRequired, NumberRange

class AppointmentResponseForm(FlaskForm):
    select_confirmation = RadioField('Acceptance:', choices=[(1,'Accept'),(-1,'Decline')], validators=[DataRequired()])