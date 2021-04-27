import users.settings as settings
from rest_framework.permissions import BasePermission


class IsNotBanned(BasePermission):
    message = 'The user is banned.'

    def has_permission(self, request, view):
        return not request.user.is_banned or settings.BAN_ALLOW_ACCOUNT


class IsOwner(BasePermission):
    message = 'Access Forbidden.'

    def has_permission(self, request, view):
        uuid = request.resolver_match.kwargs.get('pk')
        return str(request.user.uuid) == uuid
