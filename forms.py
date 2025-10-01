from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DateField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered. Please use a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AppointmentForm(FlaskForm):
    date = DateField('Appointment Date', validators=[DataRequired()], format='%Y-%m-%d')
    time = SelectField('Appointment Time', validators=[DataRequired()], 
                       choices=[('9:00 AM', '9:00 AM'), ('10:00 AM', '10:00 AM'), 
                                ('11:00 AM', '11:00 AM'), ('12:00 PM', '12:00 PM'),
                                ('2:00 PM', '2:00 PM'), ('3:00 PM', '3:00 PM'),
                                ('4:00 PM', '4:00 PM'), ('5:00 PM', '5:00 PM')])
    symptoms = TextAreaField('Symptoms/Reason for Visit', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')


class ChatbotForm(FlaskForm):
    message = StringField('Your message', validators=[DataRequired()])
    submit = SubmitField('Send')


class DoctorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    specialty = StringField('Specialty', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = IntegerField('Consultation Fee (₹)', validators=[DataRequired()])
    experience = IntegerField('Experience (years)')
    qualification = StringField('Qualifications', validators=[DataRequired()])
    availability = StringField('Availability', validators=[DataRequired()])
    submit = SubmitField('Save Doctor')

class CancelAppointmentForm(FlaskForm):
    submit = SubmitField('Cancel Appointment')


class DoctorLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class DoctorRegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    specialty = StringField('Medical Specialty', validators=[DataRequired()])
    qualification = StringField('Qualifications', validators=[DataRequired()])
    experience = IntegerField('Years of Experience', validators=[DataRequired()])
    license_number = StringField('Medical License Number', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    address = TextAreaField('Clinic/Hospital Address', validators=[DataRequired()])
    price = IntegerField('Consultation Fee (₹)', validators=[DataRequired()])
    availability = StringField('Availability (e.g., Mon-Fri 9AM-5PM)', validators=[DataRequired()])
    description = TextAreaField('Professional Summary')
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        from models import Doctor
        doctor = Doctor.query.filter_by(email=email.data).first()
        if doctor:
            raise ValidationError('Email is already registered. Please use a different one.')
    
    def validate_license_number(self, license_number):
        from models import Doctor
        doctor = Doctor.query.filter_by(license_number=license_number.data).first()
        if doctor:
            raise ValidationError('License number is already registered.')


class DoctorProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    specialty = StringField('Medical Specialty', validators=[DataRequired()])
    qualification = StringField('Qualifications', validators=[DataRequired()])
    experience = IntegerField('Years of Experience', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    address = TextAreaField('Clinic/Hospital Address', validators=[DataRequired()])
    price = IntegerField('Consultation Fee (₹)', validators=[DataRequired()])
    availability = StringField('Availability (e.g., Mon-Fri 9AM-5PM)', validators=[DataRequired()])
    description = TextAreaField('Professional Summary')
    submit = SubmitField('Update Profile')


class AppointmentStatusForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    notes = TextAreaField('Doctor\'s Notes')
    submit = SubmitField('Update Status')
