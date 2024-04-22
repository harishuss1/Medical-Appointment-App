from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, PasswordField
from wtforms.validators import DataRequired, NumberRange


class AppointmentForm(FlaskForm):
    id = IntegerField("ID:", validators=[DataRequired()])
    patient_id = IntegerField("Patient ID:", validators=[DataRequired()])
    doctor_id = IntegerField("Doctor ID:", validators=[DataRequired()])
    appointment_time = StringField(
        "Appointment Time:", validators=[DataRequired()])
    status = StringField("Status:", validators=[DataRequired()])
    location = StringField("Location:", validators=[DataRequired()])
    description = StringField("Description:", validators=[DataRequired()])
