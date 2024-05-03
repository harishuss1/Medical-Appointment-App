from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, MultipleFileField, SelectField, SelectMultipleField, FileField, StringField, IntegerField, EmailField, DateField, PasswordField, TextAreaField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo


from .db.dbmanager import get_db


class AppointmentResponseForm(FlaskForm):
    select_confirmation = RadioField('Acceptance:', choices=[(
        1, 'Accept'), (-1, 'Decline')], validators=[DataRequired()])
    room = SelectField('Room', validators=[DataRequired()], choices=[])
    
    def set_choices(self):
        rooms = get_db().get_medical_rooms()
        choices = []
        for room in rooms:
            choices.append(
                (room.room_number, f"{room.description}"))
        self.room.choices = choices


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
    patient = SelectField("Patient:", validators=[DataRequired()], choices=[], render_kw={'disabled': 'disabled'})
    doctor = SelectField("Doctor:", validators=[DataRequired()], choices=[])
    appointment_time = DateField(
        "Appointment Time:", validators=[DataRequired()])
    location = SelectField("Location:", validators=[DataRequired()])
    description = StringField("Description:", validators=[DataRequired()])
    
    def set_patients(self):
        patients = get_db().get_patients()
        patient_choices = []
        for patient in patients:
            patient_choices.append(
                (patient.id, f"{patient.first_name} {patient.last_name}"))
        self.patient.choices = patient_choices
        
    def set_doctors(self):
        doctors = get_db().get_doctors()
        doctor_choices = []
        for doctor in doctors:
            doctor_choices.append(
                (doctor.id, f"{doctor.first_name} {doctor.last_name}"))
        self.doctor.choices = doctor_choices
        
    def set_rooms(self):
        rooms = get_db().get_medical_rooms()
        choices = []
        for room in rooms:
            choices.append(
                (room.room_number, f"{room.description}"))
        self.location.choices = choices


class NoteForm(FlaskForm):

    patient = SelectField('Patient', validators=[DataRequired()], choices=[])
    note = TextAreaField('Note', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    attachement = MultipleFileField('Attachement')

    def set_choices(self):
        patients = get_db().get_patients_by_doctor(current_user.id)
        choices = []
        for patient in patients:
            choices.append(
                (patient.id, f"{patient.first_name} {patient.last_name}"))
        self.patient.choices = choices


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
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    user_type = SelectField(
        'User Type',
        choices=[('PATIENT', 'Patient'), ('STAFF', 'Staff'),
                 ('ADMIN_USER', 'Admin User'), ('ADMIN', 'Admin')],
        validators=[DataRequired()]
    )
    avatar_path = StringField('Avatar Path', validators=[])
    submit = SubmitField('Add User')


class DeleteUserForm(FlaskForm):
    email = EmailField('User Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Delete User')


class ChangeUserRoleForm(FlaskForm):
    email = EmailField('User Email', validators=[DataRequired(), Email()])
    user_type = SelectField(
        'New Role',
        choices=[('PATIENT', 'Patient'), ('STAFF', 'Staff'),
                 ('ADMIN_USER', 'Admin User'), ('ADMIN', 'Admin')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Change Role')

# added comment to fix git issue, please remove this comment later


class PatientDetailsForm(FlaskForm):
    dob = DateField('Date of Birth', validators=[DataRequired()])
    blood_type = SelectField('Blood Type', choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), (
        'B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], validators=[DataRequired()])
    height = FloatField('Height (in cm)', validators=[DataRequired()])
    weight = FloatField('Weight (in kg)', validators=[DataRequired()])
    allergies = SelectMultipleField('Allergies', choices=[])
