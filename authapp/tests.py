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
