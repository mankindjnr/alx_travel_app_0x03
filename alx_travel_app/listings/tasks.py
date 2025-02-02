from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation_email(user_email, listing_title):
    """
    Sends a booking confirmation email.
    """
    subject = "Booking Confirmation"
    message = f"Dear Customer, your booking for {listing_title} has been confirmed!"
    sender = settings.DEFAULT_FROM_EMAIL  # Ensure you have this set in settings.py
    recipient_list = [user_email]

    send_mail(subject, message, sender, recipient_list)

    return f"Booking confirmation email sent to {user_email}"
