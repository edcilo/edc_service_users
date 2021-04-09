import secrets
import users.settings as settings
from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, ActivationToken
from .emails import AccountConfirmEmail
from .repositories import UserRepository, ActivationTokenRepository
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSignUpSerializer,
    UserConfirmSerializer,
    UserRequestConfirmEmailSerializer,
)


# Create your views here.
class CustomObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.filter()

    def get_permissions(self):
        permission_classes = []

        if self.name == 'register':
            permission_classes = ()

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], name='register')
    def register(self, request):
        serializer = UserSignUpSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if settings.ACCOUNT_CONFIRM_ON and settings.SEND_ACCOUNT_CONFIRM_EMAIL:
            create_token_and_send(user)

        return Response(None, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], name='confirm')
    def confirm(self, request):
        token_repo = ActivationTokenRepository()
        user_repo = UserRepository()

        if not settings.ACCOUNT_CONFIRM_ON:
            raise Http404

        serializer = UserConfirmSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)

        token = token_repo.check_token_and_email(serializer.data['token'], serializer.data['email'], fail=True)
        if not token.is_valid():
            raise Http404

        user = user_repo.get_user_unconfirmed(token.email, fail=True)
        user_repo.account_confirm(user)

        token.delete()
        return Response(None, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], name='request_confirm')
    def request_confirm(self, request):
        if not settings.ACCOUNT_CONFIRM_ON or not settings.SEND_ACCOUNT_CONFIRM_EMAIL:
            raise Http404

        serializer = UserRequestConfirmEmailSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.data['email'], is_active=True, confirmed=False).first()

        if user is None:
            raise Http404

        create_token_and_send(user)

        return Response(None, status=status.HTTP_200_OK)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


def create_token_and_send(user):
    token = ActivationToken.objects.create(
        email=user.email,
        token=secrets.token_hex(32),
        lifetime=settings.ACCOUNT_CONFIRM_TOKEN_LIFETIME
    )

    context = {
        'link': "{}?token={}&email={}".format(settings.ACCOUNT_CONFIRM_URL, token.token, user.email)
    }
    email = AccountConfirmEmail(context, user)
    email.send()
