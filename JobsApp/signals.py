# your_app/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User, Jobseeker, Employer

@receiver(post_save, sender=User)
def send_user_signup_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Welcome to the platform!',
            f'Hi {instance.username}, your account has been successfully created.',
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )

@receiver(post_save, sender=Jobseeker)
def send_jobseeker_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Jobseeker Profile Created',
            f'Hi {instance.name.username}, your jobseeker profile has been created!',
            settings.DEFAULT_FROM_EMAIL,
            [instance.name.email],
            fail_silently=False,
        )

@receiver(post_save, sender=Employer)
def send_employer_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Employer Profile Created',
            f'Hi {instance.user.username}, your employer profile has been created!',
            settings.DEFAULT_FROM_EMAIL,
            [instance.user.email],
            fail_silently=False,
        )
