from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .views import RegisterView


class UserRegistrationTest(APITestCase):
    def test_user_registration_success(self):
        """
        Test successful user registration with valid data.
        """
        url = reverse(RegisterView.view_name)
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, data['username'])
        self.assertEqual(User.objects.get().email, data['email'])
        # TODO: check password hash as well

    def test_user_registration_invalid_data(self):
        """
        Test registration fails with missing password.
        """
        url = reverse(RegisterView.view_name)

        data = {'username': 'testuser', 'email': 'test@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.data)

    def test_duplicate_email_registration(self):
        """
        Test registration fails if user with provided email exists.
        """
        User.objects.create_user(
            username='existing', email='test@example.com', password='testpass123')

        url = reverse(RegisterView.view_name)
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.data)

    def test_duplicate_username_registration(self):
        """
        Test registration fails if user with provided username exists.
        """
        User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123')

        url = reverse(RegisterView.view_name)
        data = {
            'username': 'testuser',
            'email': 'new@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('username', response.data)


class UserAuthenticationTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.token_url = reverse('token-obtain-pair')

    def test_token_obtainment_success(self):
        """
        Test successful JWT token acquisition with valid credentials.
        """
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_obtain_invalid_credentials(self):
        """
        Test token acquisition fails with invalid credentials.
        """
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, 401)
