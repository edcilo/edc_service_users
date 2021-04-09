import secrets
import users.settings as settings
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.http import Http404
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSignUpSerializer,
    UserConfirmSerializer,
    UserRequestConfirmEmailSerializer,
)
from .models import User, ActivationToken


# Create your views here.
def create_token_and_send(user):
    token = ActivationToken.objects.create(
        email=user.email,
        token=secrets.token_hex(32),
        lifetime=settings.USERS_ACTIVATION_TOKEN_LIFETIME
    )

    context = {
        'link': "{}?token={}&email={}".format(settings.USERS_ACTIVATION_URL, token.token, user.email)
    }
    email_html_message = render_to_string('emails/user_activation_token.html', context)
    email_plaintext_message = render_to_string('emails/user_activation_token.txt', context)
    msg = EmailMultiAlternatives(
        "Activate your account for {title}".format(title="edcilo.com"),
        email_plaintext_message,
        "noreply@edcilo.com",
        [user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


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

        if settings.USERS_ACTIVATION_ON and settings.USERS_SEND_ACTIVATION_EMAIL:
            create_token_and_send(user)

        return Response(None, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], name='confirm')
    def confirm(self, request):
        serializer = UserConfirmSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)

        try:
            token = ActivationToken.objects.filter(
                token=serializer.data['token'],
                email=serializer.data['email']
            ).first()

            if token.is_valid():
                user = User.objects.filter(email=token.email, is_active=False, deleted=False).first()
                user.is_active = True
                user.activated_at = timezone.now()
                user.save()
            else:
                raise Http404

            token.delete()
        except (ActivationToken.DoesNotExist, User.DoesNotExist,):
            raise Http404

        return Response(None, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], name='request_confirm')
    def request_confirm(self, request):
        serializer = UserRequestConfirmEmailSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.filter(email=serializer.data['email'], is_active=False, deleted=False).first()
        except User.DoesNotExist:
            raise Http404

        if not user is None:
            create_token_and_send(user)
        else:
            raise Http404

        return Response(None, status=status.HTTP_200_OK)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        print('--------------------->', settings.USERS_ACTIVATION_ON)
        return Response(content)
