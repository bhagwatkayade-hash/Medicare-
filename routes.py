from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from models import User, Doctor, Appointment
from forms import (RegistrationForm, LoginForm, AppointmentForm, ChatbotForm, DoctorForm, 
                   CancelAppointmentForm, DoctorLoginForm, DoctorRegistrationForm, 
                   DoctorProfileForm, AppointmentStatusForm)
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
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
def manage_doctors():
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
        return redirect(url_for('manage_doctors'))
    
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
        return redirect(url_for('manage_doctors'))
    
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
        return redirect(url_for('manage_doctors'))
    
    db.session.delete(doctor)
    db.session.commit()
    flash('Doctor has been deleted!', 'success')
    return redirect(url_for('manage_doctors'))

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
                'email': 'sharma@medicareplus.com',
                'specialty': 'Cardiologist',
                'description': 'Specialized in heart diseases with over 15 years of experience.',
                'price': 1500,
                'experience': 15,
                'qualification': 'MD, DM Cardiology',
                'availability': 'Mon-Fri, 9 AM - 5 PM',
                'phone': '+91-9876543210',
                'address': 'Heart Care Clinic, Mumbai',
                'license_number': 'MH12345',
                'is_verified': True
            },
            {
                'name': 'Dr. Patel',
                'email': 'patel@medicareplus.com',
                'specialty': 'Pediatrician',
                'description': 'Child specialist with a focus on newborn care.',
                'price': 1200,
                'experience': 10,
                'qualification': 'MBBS, MD Pediatrics',
                'availability': 'Mon-Sat, 10 AM - 6 PM',
                'phone': '+91-9876543211',
                'address': 'Children\'s Hospital, Delhi',
                'license_number': 'DL12346',
                'is_verified': True
            },
            {
                'name': 'Dr. Gupta',
                'email': 'gupta@medicareplus.com',
                'specialty': 'Orthopedic Surgeon',
                'description': 'Expert in joint replacements and sports injuries.',
                'price': 1800,
                'experience': 12,
                'qualification': 'MS Orthopedics, Fellowship in Joint Replacement',
                'availability': 'Tue-Sat, 11 AM - 7 PM',
                'phone': '+91-9876543212',
                'address': 'Bone & Joint Clinic, Bangalore',
                'license_number': 'KA12347',
                'is_verified': True
            },
            {
                'name': 'Dr. Mehta',
                'email': 'mehta@medicareplus.com',
                'specialty': 'Dermatologist',
                'description': 'Specialist in skin disorders and cosmetic procedures.',
                'price': 1600,
                'experience': 8,
                'qualification': 'MD Dermatology',
                'availability': 'Mon, Wed, Fri, 9 AM - 3 PM',
                'phone': '+91-9876543213',
                'address': 'Skin Care Center, Chennai',
                'license_number': 'TN12348',
                'is_verified': True
            },
            {
                'name': 'Dr. Singh',
                'email': 'singh@medicareplus.com',
                'specialty': 'Neurologist',
                'description': 'Specializes in brain and nervous system disorders.',
                'price': 2000,
                'experience': 18,
                'qualification': 'MD, DM Neurology',
                'availability': 'Mon-Thu, 10 AM - 4 PM',
                'phone': '+91-9876543214',
                'address': 'Neuro Care Hospital, Kolkata',
                'license_number': 'WB12349',
                'is_verified': True
            }
        ]
        
        for doctor_data in doctors:
            doctor = Doctor(**doctor_data)
            doctor.set_password('doctor123')  # Default password for sample doctors
            db.session.add(doctor)
        
        db.session.commit()
        logging.info('Initial doctors data created')


# Doctor Authentication Routes
@app.route('/doctor/login', methods=['GET', 'POST'])
def doctor_login():
    if current_user.is_authenticated and isinstance(current_user, Doctor):
        return redirect(url_for('doctor_dashboard'))
    
    form = DoctorLoginForm()
    if form.validate_on_submit():
        doctor = Doctor.query.filter_by(email=form.email.data).first()
        if doctor and doctor.check_password(form.password.data):
            login_user(doctor, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('doctor_dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('doctor/login.html', title='Doctor Login', form=form)


@app.route('/doctor/register', methods=['GET', 'POST'])
def doctor_register():
    if current_user.is_authenticated and isinstance(current_user, Doctor):
        return redirect(url_for('doctor_dashboard'))
    
    form = DoctorRegistrationForm()
    if form.validate_on_submit():
        doctor = Doctor(
            name=form.name.data,
            email=form.email.data,
            specialty=form.specialty.data,
            qualification=form.qualification.data,
            experience=form.experience.data,
            license_number=form.license_number.data,
            phone=form.phone.data,
            address=form.address.data,
            price=form.price.data,
            availability=form.availability.data,
            description=form.description.data,
            is_verified=True,  # Auto-verify for direct registration
            is_active=True     # Auto-activate account
        )
        doctor.set_password(form.password.data)
        
        db.session.add(doctor)
        db.session.commit()
        
        flash('Registration successful! You can now login with your credentials.', 'success')
        return redirect(url_for('doctor_login'))
    
    return render_template('doctor/register.html', title='Doctor Registration', form=form)


@app.route('/doctor/logout')
@login_required
def doctor_logout():
    logout_user()
    return redirect(url_for('index'))


# Doctor Dashboard and Management Routes
@app.route('/doctor/dashboard')
@login_required
def doctor_dashboard():
    if not isinstance(current_user, Doctor):
        abort(403)
    
    # Get today's appointments
    today = datetime.now().date()
    today_appointments = Appointment.query.filter_by(
        doctor_id=current_user.id,
        date=today
    ).order_by(Appointment.time).all()
    
    # Get upcoming appointments
    upcoming_appointments = Appointment.query.filter(
        Appointment.doctor_id == current_user.id,
        Appointment.date > today
    ).order_by(Appointment.date, Appointment.time).limit(5).all()
    
    # Get statistics
    total_appointments = Appointment.query.filter_by(doctor_id=current_user.id).count()
    pending_appointments = Appointment.query.filter_by(
        doctor_id=current_user.id,
        status='Pending'
    ).count()
    confirmed_appointments = Appointment.query.filter_by(
        doctor_id=current_user.id,
        status='Confirmed'
    ).count()
    
    return render_template('doctor/dashboard.html',
                         title='Doctor Dashboard',
                         today_appointments=today_appointments,
                         upcoming_appointments=upcoming_appointments,
                         total_appointments=total_appointments,
                         pending_appointments=pending_appointments,
                         confirmed_appointments=confirmed_appointments,
                         today=today)


@app.route('/doctor/appointments')
@login_required
def doctor_appointments():
    if not isinstance(current_user, Doctor):
        abort(403)
    
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    
    query = Appointment.query.filter_by(doctor_id=current_user.id)
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    appointments = query.order_by(Appointment.date.desc(), Appointment.time.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('doctor/appointments.html',
                         title='My Appointments',
                         appointments=appointments,
                         status_filter=status_filter)


@app.route('/doctor/appointment/<int:appointment_id>')
@login_required
def doctor_appointment_detail(appointment_id):
    if not isinstance(current_user, Doctor):
        abort(403)
    
    appointment = Appointment.query.filter_by(
        id=appointment_id,
        doctor_id=current_user.id
    ).first_or_404()
    
    return render_template('doctor/appointment_detail.html',
                         title='Appointment Details',
                         appointment=appointment)


@app.route('/doctor/appointment/<int:appointment_id>/update', methods=['GET', 'POST'])
@login_required
def doctor_update_appointment(appointment_id):
    if not isinstance(current_user, Doctor):
        abort(403)
    
    appointment = Appointment.query.filter_by(
        id=appointment_id,
        doctor_id=current_user.id
    ).first_or_404()
    
    form = AppointmentStatusForm()
    
    if form.validate_on_submit():
        appointment.status = form.status.data
        if hasattr(appointment, 'notes'):
            appointment.notes = form.notes.data
        else:
            # Add notes column if it doesn't exist
            pass
        
        db.session.commit()
        flash('Appointment status updated successfully!', 'success')
        return redirect(url_for('doctor_appointment_detail', appointment_id=appointment.id))
    
    # Pre-populate form
    if request.method == 'GET':
        form.status.data = appointment.status
        if hasattr(appointment, 'notes'):
            form.notes.data = appointment.notes
    
    return render_template('doctor/update_appointment.html',
                         title='Update Appointment',
                         appointment=appointment,
                         form=form)


@app.route('/doctor/profile')
@login_required
def doctor_profile():
    if not isinstance(current_user, Doctor):
        abort(403)
    
    return render_template('doctor/profile.html',
                         title='My Profile',
                         doctor=current_user)


@app.route('/doctor/profile/edit', methods=['GET', 'POST'])
@login_required
def doctor_edit_profile():
    if not isinstance(current_user, Doctor):
        abort(403)
    
    form = DoctorProfileForm()
    
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.specialty = form.specialty.data
        current_user.qualification = form.qualification.data
        current_user.experience = form.experience.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        current_user.price = form.price.data
        current_user.availability = form.availability.data
        current_user.description = form.description.data
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('doctor_profile'))
    
    # Pre-populate form
    if request.method == 'GET':
        form.name.data = current_user.name
        form.specialty.data = current_user.specialty
        form.qualification.data = current_user.qualification
        form.experience.data = current_user.experience
        form.phone.data = current_user.phone
        form.address.data = current_user.address
        form.price.data = current_user.price
        form.availability.data = current_user.availability
        form.description.data = current_user.description
    
    return render_template('doctor/edit_profile.html',
                         title='Edit Profile',
                         form=form)


@app.route('/doctor/schedule')
@login_required
def doctor_schedule():
    if not isinstance(current_user, Doctor):
        abort(403)
    
    # Get appointments for the next 7 days
    today = datetime.now().date()
    week_from_today = today + timedelta(days=7)
    
    appointments = Appointment.query.filter(
        Appointment.doctor_id == current_user.id,
        Appointment.date >= today,
        Appointment.date <= week_from_today
    ).order_by(Appointment.date, Appointment.time).all()
    
    # Group appointments by date
    schedule = {}
    for appointment in appointments:
        date_str = appointment.date.strftime('%Y-%m-%d')
        if date_str not in schedule:
            schedule[date_str] = []
        schedule[date_str].append(appointment)
    
    return render_template('doctor/schedule.html',
                         title='Weekly Schedule',
                         schedule=schedule,
                         today=today)
