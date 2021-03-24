import users.settings as settings
import uuid
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


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

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()

        super().save(*args, **kwargs)


class ActivationToken(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    lifetime = models.PositiveSmallIntegerField(default=settings.USERS_ACTIVATION_TOKEN_LIFETIME)

    def __str__(self):
        return self.email

    def is_valid(self):
        limit = self.created + timedelta(seconds=self.lifetime)
        now = timezone.now()
        return limit > now
