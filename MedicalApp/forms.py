from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, IntegerField, EmailField, DateField, PasswordField, TextAreaField , SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from .db.dbmanager import get_db


class AppointmentResponseForm(FlaskForm):
    select_confirmation = RadioField('Acceptance:', choices=[(
        1, 'Accept'), (-1, 'Decline')], validators=[DataRequired()])


class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long'),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = EmailField('email')
    password = PasswordField('password')


class AppointmentForm(FlaskForm):
    id = IntegerField("ID:", validators=[DataRequired()])
    patient_id = IntegerField("Patient ID:", validators=[DataRequired()])
    doctor_id = IntegerField("Doctor ID:", validators=[DataRequired()])
    appointment_time = StringField(
        "Appointment Time:", validators=[DataRequired()])
    status = StringField("Status:", validators=[DataRequired()])
    location = StringField("Location:", validators=[DataRequired()])
    description = StringField("Description:", validators=[DataRequired()])
    
class NoteForm(FlaskForm):
    
    patient = SelectField('Patient', validators=[DataRequired()], choices=[])
    note = TextAreaField('Note', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    attachement = FileField('Attachement')
    
    def set_choices(self):
        patients = get_db().get_patients_by_doctor(current_user.id)
        choices = []
        for patient in patients:
            choices.append((patient.id, f"{patient.first_name} {patient.last_name}"))
        self.patient.choices = choices
    
