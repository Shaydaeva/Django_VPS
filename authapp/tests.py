from django.test import TestCase, Client

from authapp.models import ShopUser


class TestUserAuthTestCase(TestCase):
    def setUp(self):
        self.admin = ShopUser.objects.create_superuser('django', 'django@gb.local', 'geekbrains')
        self.client = Client()

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertNotContains(response, 'Пользователь')
