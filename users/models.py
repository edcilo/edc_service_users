from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    phone = models.CharField(null=True, max_length=20)
    activated_at = models.DateTimeField(null=True)
    metadata = models.JSONField(null=True)
    updated_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)
