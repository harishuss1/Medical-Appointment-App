from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, PasswordField, SubmitField, RadioField, SelectField
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
    
class BlockUserForm(FlaskForm):
    email = EmailField('User Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Block User')

class AddUserForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long'),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    user_type = SelectField(
        'User Type',
        choices=[('PATIENT', 'Patient'), ('STAFF', 'Staff'), ('ADMIN_USER', 'Admin User'), ('ADMIN', 'Admin')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Add User')

class DeleteUserForm(FlaskForm):
    email = EmailField('User Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Delete User')

class ChangeUserRoleForm(FlaskForm):
    email = EmailField('User Email', validators=[DataRequired(), Email()])
    user_type = SelectField(
        'New Role',
        choices=[('PATIENT', 'Patient'), ('STAFF', 'Staff'), ('ADMIN_USER', 'Admin User'), ('ADMIN', 'Admin')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Change Role')