import re

# Simple rule-based chatbot for healthcare assistance
def get_chatbot_response(message):
    # Convert message to lowercase for easier matching
    message = message.lower()
    
    # Common greetings
    if re.search(r'(hello|hi|hey|greetings)', message):
        return "Hello! I'm your Medicare assistant. How can I help you today?"
    
    # About appointment booking
    elif re.search(r'(book|schedule|make|appointment)', message):
        return "To book an appointment, please browse our list of doctors, select one, and click on 'Book Appointment'. You'll need to be logged in to complete the booking."
    
    # About doctors
    elif re.search(r'(doctor|specialist|physician)', message):
        return "We have specialists in various fields including cardiology, pediatrics, orthopedics, dermatology, and neurology. You can view all our doctors and their specialties on the Doctors page."
    
    # About pricing
    elif re.search(r'(price|cost|fee|fees|charges)', message):
        return "Each doctor has their own consultation fee which is displayed on their profile. The fees typically range from ₹1000 to ₹2500 depending on the specialization."
    
    # About cancellation
    elif re.search(r'(cancel|reschedule|change|appointment)', message):
        return "You can cancel or reschedule your appointment by going to 'My Appointments' section after logging in. Please note that cancellations should be made at least 24 hours before the appointment time."
    
    # About registration
    elif re.search(r'(register|sign up|create account)', message):
        return "To register, click on the 'Sign Up' link in the navigation bar. You'll need to provide a username, email address, and password."
    
    # About login issues
    elif re.search(r'(login|sign in|password|forgot)', message):
        return "To log in, use your registered email and password. If you've forgotten your password, please contact our support team."
    
    # About medical conditions (general response)
    elif re.search(r'(symptom|pain|fever|cough|cold|headache|migraine)', message):
        return "I'm not qualified to provide medical advice. If you're experiencing symptoms, please book an appointment with an appropriate specialist."
    
    # About COVID-19
    elif re.search(r'(covid|corona|virus|pandemic)', message):
        return "For COVID-19 related queries, please consult our specialists. We follow all safety protocols during appointments. If you have symptoms, please inform us in advance."
    
    # For emergency situations
    elif re.search(r'(emergency|urgent|critical|ambulance)', message):
        return "If you're experiencing a medical emergency, please call emergency services (102/108/112) immediately. Our chatbot is not equipped to handle emergency situations."
    
    # Default response
    else:
        return "I'm sorry, I didn't understand your query. Could you please rephrase or ask something about appointments, doctors, or our services?"
