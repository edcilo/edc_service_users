from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User, Ban, BanReason


# Create your tests here.
class UserTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='edcilo', email='test@edcilo.com', password='secret123', confirmed=True)

    def login(self, email, password):
        data = {'email': email, 'password': password}
        url = reverse('users:token_obtain_pair')
        return self.client.post(url, data, format='json')

    def test_login_to_confirmed_user(self):
        response = self.login('test@edcilo.com', 'secret123')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_to_unconfirmed_user(self):
        User.objects.create_user(
            username='unconfirmed_user',
            email='unconfirmed_user@edcilo.com',
            password='secret123',
            confirmed=False
        )
        response = self.login('unconfirmed_user@edcilo.com', 'secret123')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_to_banned_user(self):
        test_user = User.objects.get(pk=1)
        test_ban_reason = BanReason.objects.create(code='001', description='lorem ipsum', days=7)
        test_ban = Ban.objects.create(
            user=test_user,
            reason=test_ban_reason,
            description='First strike',
            banned_at=timezone.now() - timedelta(2)
        )
        strike = test_user.strikes.first()
        response = self.login('test@edcilo.com', 'secret123')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_refresh_token(self):
        response = self.login('test@edcilo.com', 'secret123')
        token = response.json()['refresh']
        data = {'refresh': token}
        url = reverse('users:token_refresh')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_token(self):
        response = self.login('test@edcilo.com', 'secret123')
        token = response.json()['access']
        data = {'token': token}
        url = reverse('users:token_verify')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register(self):
        data = {
            'email': 'new_user@edcilo.com',
            'username': 'new_user',
            'password': 'secret123.',
            'password_confirmation': 'secret123.'
        }
        url = reverse('users:account-register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_public_user(self):
        test_user = User.objects.get(pk=1)
        uuid = test_user.uuid
        url = reverse('users:user', args=(uuid,))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dont_access_to_user_profile(self):
        test_user = User.objects.create_user(
            username='unconfirmed_user',
            email='unconfirmed_user@edcilo.com',
            password='secret123',
            confirmed=True,
            public=False
        )
        uuid = test_user.uuid
        url = reverse('users:user', args=(uuid,))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
