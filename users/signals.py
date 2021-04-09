from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django_rest_resetpassword.signals import reset_password_token_created
from .emails import PasswordResetTokenCreatedEmail

"""
from .models import User

@receiver(pre_save, sender=User)
def set_new_user_inactive(sender, instance, **kwargs):
    if instance._state.adding is True:
        instance.confirmed = False
"""


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    reset_password_url = "{}?token={}".format(
        reverse('users:password_reset:reset-password-request'),
        reset_password_token.key
    )
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': reset_password_url,
    }
    email = PasswordResetTokenCreatedEmail(context, reset_password_token)
    email.send()

