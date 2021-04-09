from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException
from rest_framework import status


class AccountNotConfirmedAPIException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Account not confirmed.')
    default_code = 'authentication_failed'
