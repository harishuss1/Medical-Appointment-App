from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, IntegerField, EmailField, PasswordField, TextAreaField , SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from MedicalApp.db.dbmanager import get_db


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
    def get_choices():
        patients = get_db().get_patients_by_doctor(current_user.id)
        choices = []
        for patient in patients:
            choices.append((patient.id, "{patient.first_name} {patient.last_name}"))
        return choices
    
    patient = SelectField('Patient', validators=[DataRequired()], choices=get_choices())
    note = TextAreaField('Note', validators=[DataRequired()], choices=get_choices())
    attachement = FileField('Attachement')
    
