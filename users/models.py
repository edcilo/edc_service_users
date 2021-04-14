# https://github.com/django/django/blob/main/django/contrib/auth/models.py
import users.settings as settings
import uuid
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.http import Http404
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(null=True, max_length=20, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_banned(self):
        now = timezone.now()
        current_strikes = self.strikes.filter(active=True, banned_at__lte=now, banned_until__gte=now).count()
        total_strikes = self.strikes.filter(active=True).count()
        return current_strikes > 0 or total_strikes >= settings.BAN_STRIKES_ALLOWED

    @property
    def ban_info(self):
        now = timezone.now()
        ban = self.strikes.filter(active=True, banned_at__lte=now, banned_until__gte=now).first()

        return {
            'is_banned': ban is not None,
            'strikes': self.strikes.filter(active=True).count(),
            'banned_until': None if ban is None else ban.banned_until.isoformat(),
            'banned_reason': None if ban is None else ban.reason.description,
        }

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()

        super().save(*args, **kwargs)


class ActivationToken(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    lifetime = models.PositiveSmallIntegerField(default=settings.ACCOUNT_CONFIRM_TOKEN_LIFETIME)

    def __str__(self):
        return self.email

    def is_valid(self, raise_exception=False):
        limit = self.created + timedelta(seconds=self.lifetime)
        now = timezone.now()
        is_valid = limit > now
        if raise_exception and not is_valid:
            raise Http404
        return is_valid


class BanReason(models.Model):
    code = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    days = models.IntegerField()

    def __str__(self):
        return "%s - %s" % (self.code, self.description)


class Ban(models.Model):
    active = models.BooleanField(default=True)
    banned_at = models.DateTimeField()
    banned_until = models.DateTimeField(null=True, blank=True)
    description = models.TextField()
    reason = models.ForeignKey(BanReason, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='strikes')

    def __str__(self):
        return self.description
