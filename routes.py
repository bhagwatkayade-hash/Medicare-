from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from models import User, Doctor, Appointment
from forms import RegistrationForm, LoginForm, AppointmentForm, ChatbotForm, DoctorForm, CancelAppointmentForm
from werkzeug.security import generate_password_hash
from datetime import datetime
from chatbot import get_chatbot_response
import logging

# Home route
@app.route('/')
def index():
    return render_template('index.html', title='Home')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        # First user becomes admin
        if User.query.count() == 0:
            user.is_admin = True
            
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check your email and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)

# Logout route
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

# Doctors listing route
@app.route('/doctors')
def doctors():
    all_doctors = Doctor.query.all()
    return render_template('doctors.html', title='Our Doctors', doctors=all_doctors)

# Book appointment route
@app.route('/book_appointment/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def book_appointment(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    form = AppointmentForm()
    
    if form.validate_on_submit():
        # Check if appointment already exists
        existing_appointment = Appointment.query.filter_by(
            doctor_id=doctor_id,
            date=form.date.data,
            time=form.time.data
        ).first()
        
        if existing_appointment:
            flash('This appointment slot is already booked. Please select another time.', 'danger')
        else:
            appointment = Appointment(
                user_id=current_user.id,
                doctor_id=doctor_id,
                date=form.date.data,
                time=form.time.data,
                symptoms=form.symptoms.data,
                status='Pending'
            )
            db.session.add(appointment)
            db.session.commit()
            flash(f'Appointment booked with Dr. {doctor.name} on {appointment.date} at {appointment.time}', 'success')
            return redirect(url_for('my_appointments'))
    
    return render_template('book_appointment.html', title='Book Appointment', form=form, doctor=doctor)

# My appointments route
@app.route('/my_appointments')
@login_required
def my_appointments():
    appointments = Appointment.query.filter_by(user_id=current_user.id).order_by(Appointment.date.desc()).all()
    today = datetime.now().date()
    cancel_form = CancelAppointmentForm()
    return render_template('my_appointments.html', title='My Appointments', appointments=appointments, today=today, form=cancel_form)

# Cancel appointment route
@app.route('/cancel_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if appointment.user_id != current_user.id:
        abort(403)  # Forbidden
    
    appointment.status = 'Cancelled'
    db.session.commit()
    flash('Your appointment has been cancelled.', 'info')
    return redirect(url_for('my_appointments'))

# Chatbot route
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    form = ChatbotForm()
    return render_template('chat.html', title='Health Assistant', form=form)

# Chatbot API endpoint
@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.json
    user_message = data.get('message', '')
    response = get_chatbot_response(user_message)
    return jsonify({"response": response})

# Admin routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    total_users = User.query.count()
    total_doctors = Doctor.query.count()
    total_appointments = Appointment.query.count()
    pending_appointments = Appointment.query.filter_by(status='Pending').count()
    
    return render_template('admin/dashboard.html', title='Admin Dashboard',
                          total_users=total_users,
                          total_doctors=total_doctors,
                          total_appointments=total_appointments,
                          pending_appointments=pending_appointments)

@app.route('/admin/doctors', methods=['GET'])
@login_required
def admin_doctors():
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    doctors = Doctor.query.all()
    return render_template('admin/manage_doctors.html', title='Manage Doctors', doctors=doctors)

@app.route('/admin/doctors/add', methods=['GET', 'POST'])
@login_required
def add_doctor():
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    form = DoctorForm()
    if form.validate_on_submit():
        doctor = Doctor(
            name=form.name.data,
            specialty=form.specialty.data,
            description=form.description.data,
            price=form.price.data,
            experience=form.experience.data,
            qualification=form.qualification.data,
            availability=form.availability.data
        )
        db.session.add(doctor)
        db.session.commit()
        flash('New doctor has been added!', 'success')
        return redirect(url_for('admin_doctors'))
    
    return render_template('admin/manage_doctors.html', title='Add Doctor', form=form, action="add")

@app.route('/admin/doctors/edit/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def edit_doctor(doctor_id):
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    doctor = Doctor.query.get_or_404(doctor_id)
    form = DoctorForm()
    
    if form.validate_on_submit():
        doctor.name = form.name.data
        doctor.specialty = form.specialty.data
        doctor.description = form.description.data
        doctor.price = form.price.data
        doctor.experience = form.experience.data
        doctor.qualification = form.qualification.data
        doctor.availability = form.availability.data
        
        db.session.commit()
        flash('Doctor information has been updated!', 'success')
        return redirect(url_for('admin_doctors'))
    
    # Pre-populate form with existing data
    if request.method == 'GET':
        form.name.data = doctor.name
        form.specialty.data = doctor.specialty
        form.description.data = doctor.description
        form.price.data = doctor.price
        form.experience.data = doctor.experience
        form.qualification.data = doctor.qualification
        form.availability.data = doctor.availability
    
    return render_template('admin/manage_doctors.html', title='Edit Doctor', form=form, doctor=doctor, action="edit")

@app.route('/admin/doctors/delete/<int:doctor_id>', methods=['POST'])
@login_required
def delete_doctor(doctor_id):
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    doctor = Doctor.query.get_or_404(doctor_id)
    
    # Check if doctor has any appointments
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).first()
    if appointments:
        flash('Cannot delete doctor with existing appointments.', 'danger')
        return redirect(url_for('admin_doctors'))
    
    db.session.delete(doctor)
    db.session.commit()
    flash('Doctor has been deleted!', 'success')
    return redirect(url_for('admin_doctors'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Initialize the database with some doctors if they don't exist
def create_initial_data():
    if Doctor.query.count() == 0:
        doctors = [
            {
                'name': 'Dr. Sharma',
                'specialty': 'Cardiologist',
                'description': 'Specialized in heart diseases with over 15 years of experience.',
                'price': 1500,
                'experience': 15,
                'qualification': 'MD, DM Cardiology',
                'availability': 'Mon-Fri, 9 AM - 5 PM'
            },
            {
                'name': 'Dr. Patel',
                'specialty': 'Pediatrician',
                'description': 'Child specialist with a focus on newborn care.',
                'price': 1200,
                'experience': 10,
                'qualification': 'MBBS, MD Pediatrics',
                'availability': 'Mon-Sat, 10 AM - 6 PM'
            },
            {
                'name': 'Dr. Gupta',
                'specialty': 'Orthopedic Surgeon',
                'description': 'Expert in joint replacements and sports injuries.',
                'price': 1800,
                'experience': 12,
                'qualification': 'MS Orthopedics, Fellowship in Joint Replacement',
                'availability': 'Tue-Sat, 11 AM - 7 PM'
            },
            {
                'name': 'Dr. Mehta',
                'specialty': 'Dermatologist',
                'description': 'Specialist in skin disorders and cosmetic procedures.',
                'price': 1600,
                'experience': 8,
                'qualification': 'MD Dermatology',
                'availability': 'Mon, Wed, Fri, 9 AM - 3 PM'
            },
            {
                'name': 'Dr. Singh',
                'specialty': 'Neurologist',
                'description': 'Specializes in brain and nervous system disorders.',
                'price': 2000,
                'experience': 18,
                'qualification': 'MD, DM Neurology',
                'availability': 'Mon-Thu, 10 AM - 4 PM'
            }
        ]
        
        for doctor_data in doctors:
            doctor = Doctor(**doctor_data)
            db.session.add(doctor)
        
        db.session.commit()
        logging.info('Initial doctors data created')
