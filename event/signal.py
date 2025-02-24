from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import RSVP

@receiver(post_save, sender=RSVP)
def send_rsvp_confirmation_email(sender, instance, created, **kwargs):
    if created:
        event = instance.event
        user = instance.user

        if not user.email:
            return

        subject = f'RSVP Confirmation for {event.name}'
        message = (
            f'Hello {user.get_full_name() or user.username},\n\n'
            f'You have successfully RSVPed for:\n'
            f'Event: {event.name}\n'
            f'Date: {event.date}\n'
            f'Time: {event.time}\n'
            f'Location: {event.location}\n\n'
            f'Thank you for joining us!\n'
            f'Best regards,\nThe Event Team'
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )