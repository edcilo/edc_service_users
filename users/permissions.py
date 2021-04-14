import users.settings as settings
from rest_framework.permissions import BasePermission


class IsNotBanned(BasePermission):
    message = 'The user is banned.'

    def has_permission(self, request, view):
        print(not request.user.is_banned)
        print(settings.BAN_ALLOW_ACCOUNT)
        return not request.user.is_banned or settings.BAN_ALLOW_ACCOUNT
