from datetime import datetime
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, MultipleFileField, SelectField, SelectMultipleField, FileField, StringField, IntegerField, EmailField, DateField, PasswordField, TextAreaField, SubmitField, RadioField, SelectField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf.file import FileField, FileRequired
from .db.dbmanager import get_db



def check_date(self, field):
        if len(field.data) > datetime.today():
            raise ValidationError("You cannot book an appointment before today's date")
        
class AddMedicalRoom(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired()])

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
    patient = SelectField("Patient:", choices=[])
    doctor = SelectField("Doctor:", validators=[DataRequired()], choices=[])
    appointment_time = DateField(
        "Appointment Time:", validators=[DataRequired()], render_kw={
                                          'min': datetime.today()
                                          })
    location = SelectField("Location:")
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
    date = DateField('Date', validators=[DataRequired()], render_kw={
                                          'min' : datetime.utcnow().strftime("%Y-%m-%d")
                                          })
    attachement = MultipleFileField('Attachement')

    def set_choices(self):
        patients = get_db().get_patients_by_doctor(current_user.id)
        choices = []
        for patient in patients:
            choices.append(
                (patient.id, f"{patient.first_name} {patient.last_name}"))
        self.patient.choices = choices
        
class AddAttachementForm(FlaskForm):
    attachement = MultipleFileField('Add an attachement')

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
    dob = DateField('Date of Birth', validators=[DataRequired()], render_kw={
                                          'max': datetime.today()
                                          })
    blood_type = SelectField('Blood Type', choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), (
        'B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], validators=[DataRequired()])
    height = FloatField('Height (in cm)', validators=[DataRequired()], render_kw={
                                          'min': 0
                                          })
    weight = FloatField('Weight (in kg)', validators=[DataRequired()], render_kw={
                                          'min': 0
                                          })
    allergies = SelectMultipleField('Please enter all your allergies:', choices=[])
    
    def prefill(self):
        patient = get_db().get_patients_by_id(current_user.id)
        self.dob.data = patient.dob
        self.blood_type.data = patient.blood_type
        self.height.data = patient.height
        self.weight.data = patient.weight

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[
                                 DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[
                                     DataRequired(), EqualTo("new_password", message="Passwords must match")])
    submit = SubmitField("Change Password")


class AvatarForm(FlaskForm):
    avatar = FileField('avatar')
    submit = SubmitField('Update')
