#!/usr/bin/env python3
"""
Test script to verify doctor functionality
"""
from app import app, db
from models import User, Doctor, Appointment
from datetime import datetime

def test_doctor_functionality():
    with app.app_context():
        print("=== Testing Doctor Dashboard Functionality ===")
        
        # Test 1: Check if Doctor table exists and has proper structure
        try:
            doctors = Doctor.query.all()
            print(f"✅ Doctor table exists. Found {len(doctors)} doctors.")
            
            if doctors:
                doctor = doctors[0]
                print(f"   Sample doctor: {doctor.name} ({doctor.email})")
                print(f"   Has password_hash: {'Yes' if doctor.password_hash else 'No'}")
                print(f"   Is verified: {doctor.is_verified}")
                print(f"   Is active: {doctor.is_active}")
            
        except Exception as e:
            print(f"❌ Error accessing Doctor table: {e}")
            return False
        
        # Test 2: Check if we can create a test doctor
        try:
            test_email = "test.doctor@test.com"
            existing_doctor = Doctor.query.filter_by(email=test_email).first()
            
            if not existing_doctor:
                test_doctor = Doctor(
                    name="Test Doctor",
                    email=test_email,
                    specialty="General Medicine",
                    description="Test doctor for functionality",
                    price=1000,
                    experience=5,
                    qualification="MBBS",
                    availability="Mon-Fri 9AM-5PM",
                    phone="9999999999",
                    address="Test Address",
                    license_number="TEST123",
                    is_verified=True,
                    is_active=True
                )
                test_doctor.set_password("testpass123")
                db.session.add(test_doctor)
                db.session.commit()
                print("✅ Successfully created test doctor")
            else:
                print("✅ Test doctor already exists")
                
        except Exception as e:
            print(f"❌ Error creating test doctor: {e}")
            return False
        
        # Test 3: Test doctor authentication
        try:
            test_doctor = Doctor.query.filter_by(email="test.doctor@test.com").first()
            if test_doctor and test_doctor.check_password("testpass123"):
                print("✅ Doctor authentication working")
            else:
                print("❌ Doctor authentication failed")
                
        except Exception as e:
            print(f"❌ Error testing authentication: {e}")
            return False
        
        # Test 4: Check appointments relationship
        try:
            appointments = Appointment.query.all()
            print(f"✅ Found {len(appointments)} appointments in database")
            
            if appointments:
                appointment = appointments[0]
                print(f"   Sample appointment: Patient {appointment.user_id} with Doctor {appointment.doctor_id}")
                print(f"   Status: {appointment.status}")
                
        except Exception as e:
            print(f"❌ Error checking appointments: {e}")
            return False
            
        print("\n=== All tests completed! ===")
        return True

if __name__ == "__main__":
    test_doctor_functionality()