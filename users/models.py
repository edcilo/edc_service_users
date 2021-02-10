import uuid
from django.db import models
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_resetpassword.signals import reset_password_token_created


# Create your models here.
class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(null=True, max_length=20)
    activated_at = models.DateTimeField(null=True)
    metadata = models.JSONField(null=True)
    updated_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(reverse('users:password_reset:reset-password-request'), reset_password_token.key)
    }

    email_html_message = render_to_string('emails/user_reset_password.html', context)
    email_plaintext_message = render_to_string('emails/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        "Password Reset for {title}".format(title="edcilo.com"),
        email_plaintext_message,
        "noreply@edcilo.com",
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
