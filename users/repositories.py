from django.http import Http404
from django.utils import timezone
from users.models import User, ActivationToken


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

    def get_user_unconfirmed(self, email, fail=False):
        user = self.model.objects.filter(email=email, is_active=True, confirmed=False).first()
        if fail and user is None:
            raise Http404
        return user


class ActivationTokenRepository(Repository):
    def __init__(self):
        Repository.__init__(self, ActivationToken)

    def check_token_and_email(self, token, email, fail=False):
        token = self.model.objects.filter(token=token, email=email).first()
        if fail and token is None:
            raise Http404
        return token
