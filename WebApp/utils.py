import random
from django.core.mail import send_mail

def generate_otp():
    return str(random.randint(100000, 999999))  # Generates a 6-digit OTP

def send_otp_email(email, otp):
    subject = "Your OTP for Shop Registration"
    message = f"Your OTP for shop registration is {otp}. It is valid for 10 minutes."
    send_mail(subject, message, "jissmonraju25@gmail.com", [email])
