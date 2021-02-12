from django.test import TestCase
from django.test.client import Client

from mainapp.models import ProductCategory, Product


class TestMainappTestCase(TestCase):

    def setUp(self):
        category = ProductCategory.objects.create(
            name='Test1'
        )
        Product.objects.create(
            category=category,
            name='prod_test_1'
        )
        Product.objects.create(
            category=category,
            name='prod_test_2'
        )
        self.client = Client()

    def test_mainapp_pages(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
