import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager


# Configure logging
logging.basicConfig(level=logging.DEBUG)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)

# ✅ Ensure SECRET_KEY is always set
app.config["SECRET_KEY"] = os.environ.get("SESSION_SECRET", "dev-secret-key")

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///medicare.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize the app with the extension
db.init_app(app)

# Setup login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from models import User, Doctor
    if user_id.startswith('doctor_'):
        doctor_id = int(user_id.split('_')[1])
        return Doctor.query.get(doctor_id)
    else:
        return User.query.get(int(user_id))

# Import models and routes after app initialization
import models
import routes

with app.app_context():
    # Create all database tables
    db.create_all()
