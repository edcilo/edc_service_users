import users.settings as settings
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


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


class ActivationToken(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    lifetime = models.PositiveSmallIntegerField(default=settings.USERS_ACTIVATION_TOKEN_LIFETIME)

    def __str__(self):
        return self.email
