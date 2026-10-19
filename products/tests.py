from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Category, Product


class ProductApiTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Telefonlar')
        Product.objects.create(category=self.category, name='iPhone 15', price=1000, quantity=5)

    def test_list_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['category_name'], 'Telefonlar')

    def test_create_product(self):
        data = {'category': self.category.id, 'name': 'Samsung S24', 'price': '900.00', 'quantity': 3}
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_price_must_be_positive(self):
        data = {'category': self.category.id, 'name': 'Xato', 'price': '0', 'quantity': 1}
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search(self):
        response = self.client.get('/api/products/?search=iphone')
        self.assertEqual(response.data['count'], 1)

    def test_swagger_page(self):
        response = self.client.get('/api/docs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
