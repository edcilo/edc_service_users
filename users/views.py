import users.settings as settings
from django.conf import settings as django_settings
from django.contrib.auth.hashers import make_password
from django.http import Http404
from django.shortcuts import redirect
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .permissions import IsNotBanned, IsOwner
from .repositories import UserRepository, ActivationTokenRepository
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSignUpSerializer,
    UserConfirmSerializer,
    UserModelSerializer,
    UserRequestConfirmEmailSerializer,
    UserProfileSerializer,
    UserAccountSerializer,
    UserPasswordSerializer,
)


# Create your views here.
@api_view(['GET'])
def index(request):
    REDIRECT_TO = getattr(django_settings, 'HOME_REDIRECT_TO')
    return redirect(REDIRECT_TO)


token_repo = ActivationTokenRepository()
user_repo = UserRepository()


class CustomObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer


class AccountViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = []

        if self.name == 'profile' or self.name == 'account' or self.name == 'update_account' or self.name == 'update_password':
            permission_classes = [IsAuthenticated, IsNotBanned, IsOwner]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], name='register')
    def register(self, request):
        serializer = UserSignUpSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if settings.ACCOUNT_CONFIRM_ON and settings.SEND_ACCOUNT_CONFIRM_EMAIL:
            token_repo.new_and_notify(user)

        if settings.RETURN_TOKEN_IN_REGISTER:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

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

    @action(detail=True, methods=['put', 'delete'], name='update_account')
    def account(self, request, pk=None):
        user = request.user
        data = request.data

        if request.method == 'PUT':
            serializer = UserAccountSerializer(data=data, context={'user': user})
            serializer.is_valid(raise_exception=True)
            success = user_repo.update_account(user.uuid, data)
        elif request.method == 'DELETE':
            success = user_repo.soft_delete(user.uuid)

        if success:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(None, status=status.HTTP_304_NOT_MODIFIED)

    @action(detail=True, methods=['put'], name='update_password')
    def update_password(self, request, pk=None):
        user = request.user
        data = request.data

        serializer = UserPasswordSerializer(data=data, context={'user': user})
        serializer.is_valid(raise_exception=True)

        new_password = data['new_password']
        user.set_password(new_password)
        user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get', 'put',], name='profile')
    def profile(self, request, pk=None):
        user = request.user
        data = request.data

        if request.method == 'PUT':
            serializer = UserProfileSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            updated = user_repo.update_profile(user.uuid, data)

            if updated:
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(None, status=status.HTTP_304_NOT_MODIFIED)

        serializer = UserModelSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(APIView):
    def get(self, request, uuid=None):
        user = user_repo.get_user_by_uuid(uuid, fail=True)
        serializer = UserModelSerializer(user)
        if not serializer.data['public']:
            raise Http404
        return Response(serializer.data, status=status.HTTP_200_OK)
