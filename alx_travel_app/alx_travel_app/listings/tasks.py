# listings/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from .models import Booking


@shared_task
def send_booking_confirmation_email(booking_id: int):
    """
    Sends a simple confirmation email for a booking.
    Uses booking.user.email if available, else booking.customer_email if you have it.
    """
    try:
        booking = Booking.objects.select_related("user").get(id=booking_id)
    except Booking.DoesNotExist:
        return "booking_not_found"

    # pick recipient email
    recipient = getattr(getattr(booking, "user", None), "email", None) \
        or getattr(booking, "customer_email", None)
    if not recipient:
        return "no_recipient_email"

    subject = "Your Booking Confirmation"
    message = (
        f"Hi,\n\n"
        f"Thanks for your booking (ID: {booking.id}).\n"
        f"We’re processing it and will send you details shortly.\n\n"
        f"Cheers,\nThe Team"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL",
                           "noreply@example.com"),
        recipient_list=[recipient],
        fail_silently=False,
    )
    return "sent"
