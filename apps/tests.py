from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.models import User


class HealthCheckViewTests(APITestCase):
    def test_health_check_returns_ok(self):
        url = reverse('health-check')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': 'ok'})

    def test_health_check_rejects_post(self):
        url = reverse('health-check')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class SchemaEndpointTests(TestCase):
    def test_schema_endpoint_returns_200(self):
        response = self.client.get('/api/schema/')

        self.assertEqual(response.status_code, 200)

    def test_swagger_ui_returns_200(self):
        response = self.client.get('/api/docs/')

        self.assertEqual(response.status_code, 200)


class UserApiTests(APITestCase):
    password = 'Kuchli-parol-123'

    def make_user(self, username, **extra):
        return User.objects.create_user(username, f'{username}@example.com', self.password, **extra)

    def test_register(self):
        response = self.client.post('/api/users/', {
            'username': 'ali', 'email': 'ali@example.com', 'password': self.password,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', response.data)
        self.assertTrue(User.objects.get(username='ali').check_password(self.password))

    def test_weak_password_and_duplicate_email_rejected(self):
        self.make_user('ali')
        response = self.client.post('/api/users/', {
            'username': 'vali', 'email': 'ali@example.com', 'password': '123',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertIn('email', response.data)

    def test_anonymous_cannot_list(self):
        response = self.client.get('/api/users/')
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_user_sees_and_edits_only_self(self):
        ali, vali = self.make_user('ali'), self.make_user('vali')
        self.client.force_authenticate(ali)

        response = self.client.get('/api/users/')
        self.assertEqual([u['username'] for u in response.data['results']], ['ali'])
        self.assertEqual(self.client.get(f'/api/users/{vali.id}/').status_code, 404)

        response = self.client.patch(f'/api/users/{ali.id}/', {
            'first_name': 'Ali', 'password': 'Yangi-parol-456', 'is_staff': True,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ali.refresh_from_db()
        self.assertEqual(ali.first_name, 'Ali')
        self.assertTrue(ali.check_password('Yangi-parol-456'))
        self.assertFalse(ali.is_staff)

    def test_admin_lists_and_deletes(self):
        admin = self.make_user('admin', is_staff=True)
        ali = self.make_user('ali')
        self.client.force_authenticate(admin)

        self.assertEqual(len(self.client.get('/api/users/').data['results']), 2)
        response = self.client.delete(f'/api/users/{ali.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=ali.id).exists())


class CalculatorTests(APITestCase):
    def test_path(self):
        response = self.client.get(reverse('calculator-path', args=[5, 7]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'result': 12})

    def test_query(self):
        response = self.client.get(reverse('calculator-query'), {'n1': -3, 'n2': 7})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'result': 4})

    def test_query_invalid_returns_400(self):
        response = self.client.get(reverse('calculator-query'), {'n1': 'abc'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('n1', response.data)
        self.assertIn('n2', response.data)
