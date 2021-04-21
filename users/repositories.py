import secrets
import users.settings as settings
from django.http import Http404
from django.utils import timezone
from users.models import User, ActivationToken
from .emails import AccountConfirmEmail


class Repository(object):
    def __init__(self, model):
        self.model = model


class UserRepository(Repository):
    def __init__(self):
        Repository.__init__(self, User)

    def account_confirm(self, user):
        user.confirmed = True
        user.confirmed_at = timezone.now()
        user.save()

    def get_user_by_uuid(self, uuid, fail=False):
        user = self.model.objects.filter(uuid=uuid).first()
        if fail and user is None:
            raise Http404
        return user

    def get_user_unconfirmed(self, email, fail=False):
        user = self.model.objects.filter(email=email, is_active=True, confirmed=False).first()
        if fail and user is None:
            raise Http404
        return user


class ActivationTokenRepository(Repository):
    def __init__(self):
        Repository.__init__(self, ActivationToken)

    def new(self, email):
        token = self.model.objects.create(
            email=email,
            token=secrets.token_hex(32),
            lifetime=settings.ACCOUNT_CONFIRM_TOKEN_LIFETIME
        )
        return token

    def new_and_notify(self, user):
        token = self.new(user.email)
        context = {
            'link': "{}?token={}&email={}".format(settings.ACCOUNT_CONFIRM_URL, token.token, user.email)
        }
        email = AccountConfirmEmail(context, user)
        email.send()

    def search_by_token_and_email(self, token, email, fail=False):
        token = self.model.objects.filter(token=token, email=email).first()
        if fail and token is None:
            raise Http404
        return token
