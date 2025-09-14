from monitoring.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

def check_alarm(value):
    if value >= 42:
        print("Value is over the limit. Sending email...")
        send_email()
    return()

def send_email():
    subject = 'Test Taller'
    message = 'Warning! The temperature is over the limit'
    recepient = "estudiante@hotmail.com"
    send_mail(subject, message, EMAIL_HOST_USER, [recepient])
