# 🏥 Medicare+ - Complete Healthcare Management System

A comprehensive Flask-based healthcare management platform that connects patients with doctors, featuring appointment booking, health assistance chatbot, and professional dashboards.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🌟 Features

### 👥 **Dual User System**
- **Patients**: Registration, login, appointment booking, health queries
- **Doctors**: Professional dashboard, appointment management, profile settings
- **Admin Panel**: Complete system oversight and management

### 🤖 **AI Health Assistant**
- Intelligent chatbot for health-related queries
- Pattern-matching responses for common medical questions
- Appointment booking guidance and support
- 24/7 availability for basic health information

### 📅 **Appointment Management**
- Easy online appointment booking
- Real-time availability checking
- Appointment status tracking (Pending, Confirmed, Completed, Cancelled)
- Email notifications and reminders

### 👨‍⚕️ **Doctor Dashboard**
- Professional profile management
- Appointment scheduling and management
- Patient history and records
- Revenue and statistics tracking
- Specialization and qualification management

### 🔐 **Security Features**
- Secure password hashing with Werkzeug
- Session management with Flask-Login
- CSRF protection with Flask-WTF
- Role-based access control

### 🎨 **Modern UI/UX**
- Responsive Bootstrap design
- Mobile-friendly interface
- Professional medical theme
- Intuitive navigation and user experience

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/adiborse/Medicare-.git
   cd Medicare-
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (optional)**
   ```bash
   # Create .env file
   echo "SECRET_KEY=your-secret-key-here" > .env
   echo "DATABASE_URL=sqlite:///medicare.db" >> .env
   ```

5. **Initialize the database**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 📖 Usage Guide

### For Patients

1. **Registration**: Sign up with your email and create a secure password
2. **Browse Doctors**: View available doctors with their specializations and ratings
3. **Book Appointments**: Select preferred time slots and book appointments
4. **Health Assistant**: Use the AI chatbot for basic health queries
5. **Manage Appointments**: View, reschedule, or cancel your appointments

### For Doctors

1. **Professional Registration**: Create your doctor profile with credentials
2. **Dashboard Access**: Monitor appointments, patients, and statistics
3. **Profile Management**: Update specialization, availability, and rates
4. **Appointment Handling**: Confirm, reschedule, or manage patient appointments
5. **Patient Communication**: Access patient history and appointment notes

### For Administrators

1. **Admin Dashboard**: Overview of system statistics and user management
2. **User Management**: Monitor and manage patient and doctor accounts
3. **System Analytics**: Track appointments, revenue, and platform usage

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with SQLite
- **Authentication**: Flask-Login with password hashing
- **Forms**: Flask-WTF with CSRF protection
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Icons**: Font Awesome
- **Development**: Python 3.8+, Git version control

## 📁 Project Structure

```
Medicare-/
│
├── app.py                 # Flask application factory and configuration
├── run.py                # Application entry point
├── models.py             # Database models (User, Doctor, Appointment)
├── routes.py             # Application routes and business logic
├── forms.py              # WTForms for user input validation
├── chatbot.py            # Health assistant chatbot logic
├── requirements.txt      # Python dependencies
├── medicare.db           # SQLite database file
│
├── templates/            # Jinja2 HTML templates
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Home page
│   ├── auth/            # Authentication templates
│   ├── doctor/          # Doctor dashboard templates
│   ├── admin/           # Admin panel templates
│   └── chat.html        # Health assistant interface
│
└── static/              # Static files (CSS, JS, images)
    ├── css/
    ├── js/
    └── images/
```

## 🔧 Configuration

### Environment Variables

- `SECRET_KEY`: Flask secret key for sessions (default: auto-generated)
- `DATABASE_URL`: Database connection string (default: SQLite)
- `DEBUG`: Enable debug mode (default: True in development)

### Database Setup

The application uses SQLAlchemy with SQLite by default. For production, you can configure PostgreSQL or MySQL:

```python
# For PostgreSQL
DATABASE_URL = "postgresql://username:password@localhost/medicare"

# For MySQL
DATABASE_URL = "mysql://username:password@localhost/medicare"
```

## 🧪 Testing

### Creating Test Data

```bash
# Create a test doctor account
python -c "
from app import app, db
from models import Doctor
app.app_context().push()
doctor = Doctor(
    name='Dr. John Smith',
    email='doctor@medicare.com',
    specialty='General Medicine',
    price=1500,
    experience=10,
    qualification='MBBS, MD',
    availability='Mon-Fri 9AM-6PM',
    phone='9876543210',
    address='Medical Center, City',
    license_number='DOC12345'
)
doctor.set_password('doctor123')
db.session.add(doctor)
db.session.commit()
print('Test doctor created!')
"
```

### Test Credentials

- **Doctor Login**: doctor@medicare.com / doctor123
- **Patient**: Register a new account through the web interface

## 🚀 Deployment

### Local Development
```bash
python run.py
```

### Production Deployment

1. **Set production environment variables**
2. **Use a production WSGI server** (e.g., Gunicorn)
3. **Configure a reverse proxy** (e.g., Nginx)
4. **Set up SSL certificates** for HTTPS
5. **Use a production database** (PostgreSQL/MySQL)

Example with Gunicorn:
```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 API Endpoints

### Authentication
- `GET /` - Home page
- `GET /register` - Patient registration
- `POST /register` - Process patient registration
- `GET /login` - Patient login
- `POST /login` - Process patient login
- `GET /logout` - User logout

### Doctor System
- `GET /doctor/register` - Doctor registration
- `POST /doctor/register` - Process doctor registration
- `GET /doctor/login` - Doctor login
- `POST /doctor/login` - Process doctor login
- `GET /doctor/dashboard` - Doctor dashboard
- `GET /doctor/appointments` - Doctor appointments
- `GET /doctor/profile` - Doctor profile management

### Appointments
- `GET /doctors` - Browse available doctors
- `GET /book_appointment/<doctor_id>` - Book appointment form
- `POST /book_appointment/<doctor_id>` - Process appointment booking
- `GET /my_appointments` - User appointments
- `POST /cancel_appointment/<appointment_id>` - Cancel appointment

### Health Assistant
- `GET /chat` - Chatbot interface
- `POST /api/chat` - Chatbot API endpoint

### Admin Panel
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/users` - User management
- `GET /admin/doctors` - Doctor management

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
2. **Database Errors**: Initialize the database with the setup command
3. **Port Already in Use**: Change the port in `run.py` or kill the existing process
4. **Template Not Found**: Check that templates are in the correct directory structure

### Debug Mode

Enable detailed error messages by setting `DEBUG=True` in your environment or in `app.py`.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Aditya Borse**
- GitHub: [@adiborse](https://github.com/adiborse)
- Project Link: [https://github.com/adiborse/Medicare-](https://github.com/adiborse/Medicare-)

## 🙏 Acknowledgments

- Flask community for the excellent framework
- Bootstrap team for the responsive CSS framework
- Font Awesome for the beautiful icons
- SQLAlchemy for the powerful ORM
- All contributors and users of Medicare+

## 📞 Support

If you have any questions or need support, please:

1. Check the [Issues](https://github.com/adiborse/Medicare-/issues) page
2. Create a new issue with detailed information
3. Contact the maintainer through GitHub

---

⭐ **Star this repository if you find it helpful!** ⭐

Made with ❤️ for better healthcare accessibility
