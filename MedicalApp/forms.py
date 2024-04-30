from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, SelectField, SelectMultipleField, StringField, IntegerField, EmailField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo


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


class PatientDetailsForm(FlaskForm):
    dob = DateField('Date of Birth', validators=[DataRequired()])
    blood_type = SelectField('Blood Type', choices=[('A+', 'A+'),('A-', 'A-'), ('B+', 'B+'),('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'),('O+', 'O+'), ('O-', 'O-')], validators=[DataRequired()])
    height = FloatField('Height (in cm)', validators=[DataRequired()])
    weight = FloatField('Weight (in kg)', validators=[DataRequired()])
    allergies = SelectMultipleField('Allergies', choices=[]) 

