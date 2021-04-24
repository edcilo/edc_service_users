import users.settings as settings
from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .permissions import IsNotBanned
from .repositories import UserRepository, ActivationTokenRepository
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSignUpSerializer,
    UserConfirmSerializer,
    UserModelSerializer,
    UserRequestConfirmEmailSerializer,
    UserProfileSerializer,
)


# Create your views here.
token_repo = ActivationTokenRepository()
user_repo = UserRepository()


class CustomObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer


class AccountViewSet(viewsets.GenericViewSet):
    def get_permissions(self):
        permission_classes = []

        if self.name == 'profile':
            permission_classes = [IsAuthenticated, IsNotBanned]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], name='register')
    def register(self, request):
        serializer = UserSignUpSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if settings.ACCOUNT_CONFIRM_ON and settings.SEND_ACCOUNT_CONFIRM_EMAIL:
            token_repo.new_and_notify(user)

        return Response(None, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], name='confirm')
    def confirm(self, request):
        if not settings.ACCOUNT_CONFIRM_ON:
            raise Http404

        serializer = UserConfirmSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)

        token = token_repo.search_by_token_and_email(serializer.data['token'], serializer.data['email'], fail=True)
        token.is_valid(raise_exception=True)
        token.delete()

        user = user_repo.get_user_unconfirmed(token.email, fail=True)
        user_repo.account_confirm(user)

        return Response(None, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], name='request_confirm')
    def request_confirm(self, request):
        if not settings.ACCOUNT_CONFIRM_ON or not settings.SEND_ACCOUNT_CONFIRM_EMAIL:
            raise Http404

        serializer = UserRequestConfirmEmailSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        user = user_repo.get_user_unconfirmed(serializer.data['email'], fail=True)
        token_repo.new_and_notify(user)

        return Response(None, status=status.HTTP_200_OK)


class ProfileViewSet(APIView):
    permission_classes = [IsAuthenticated, IsNotBanned]

    def get(self, request):
        user = request.user
        serializer = UserModelSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        data = request.data

        serializer = UserProfileSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        updated = user_repo.update_profile(user.uuid, data)

        if updated:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(None, status=status.HTTP_304_NOT_MODIFIED)

    def delete(self, request):
        user = request.user
        deleted = user_repo.soft_delete(user.uuid)

        if deleted:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(None, status=status.HTTP_304_NOT_MODIFIED)


class UserViewSet(APIView):
    def get(self, request, uuid=None):
        user = user_repo.get_user_by_uuid(uuid, fail=True)
        serializer = UserModelSerializer(user)
        if not serializer.data['public']:
            raise Http404
        return Response(serializer.data, status=status.HTTP_200_OK)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
