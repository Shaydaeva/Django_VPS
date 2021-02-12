from django.conf import settings
from django.test import TestCase, Client

from authapp.models import ShopUser


class TestUserAuthTestCase(TestCase):
    username = 'django'
    email = 'django@gb.local'
    password = 'geekbrains'

    def setUp(self):
        self.admin = ShopUser.objects.create_superuser(self.username, self.email, self.password)
        self.client = Client()

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertNotContains(response, 'Пользователь')

        self.client.login(username=self.username, password=self.password)

        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.admin)

        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertContains(response, 'Пользователь')

    def test_basket_login_redirect(self):
        response = self.client.get('/basket/')
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.username, password=self.password)

        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['basket']), [])

    def test_user_register(self):
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)

        new_user_data = {
            'username': 'django2',
            'password1': self.password,
            'password2': self.password,
            'email': 'django2@gb.local',
            'age': 30,
            'first_name': 'Django2',
            'last_name': 'Django2'
        }

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 302)

        new_user = ShopUser.objects.get(username='django2')

        activation_url = f'{settings.DOMAIN}/auth/verify/{new_user_data["email"]}/{new_user.activation_key}/'

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)
