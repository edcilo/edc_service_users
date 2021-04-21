import users.settings as settings
from django.contrib.auth import password_validation
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from .exceptions import AccountNotConfirmedAPIException


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if not settings.BAN_ALLOW_LOGIN and user.is_banned:
            raise PermissionDenied()

        if settings.ACCOUNT_CONFIRM_ON and settings.ACCOUNT_CONFIRM_REQUIRED:
            if not user.is_superuser and not user.confirmed:
                raise AccountNotConfirmedAPIException()

        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['confirmed'] = user.confirmed
        token['deleted'] = not user.is_active
        token['ban'] = user.ban_info

        return token


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = (
            'uuid',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'public',
            'is_staff',
            'is_active',
            'confirmed',
            'confirmed_at',
            'deleted_at',
            'updated_at',
            'date_joined',
            'ban_info',
            'metadata',
        )


class UserSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError(_("Passwords do not match."))
        password_validation.validate_password(passwd)

        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        return user


class UserConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()


class UserRequestConfirmEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
