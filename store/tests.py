from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class StoreSmokeTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Test', slug='test')
        self.product = Product.objects.create(
            category=category,
            name='Test Product',
            slug='test-product',
            description='Test description',
            price='10.00',
            stock=5,
            is_active=True,
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_product_listing(self):
        response = self.client.get(reverse('product_list'))
        self.assertContains(response, 'Test Product')

    def test_product_detail(self):
        response = self.client.get(reverse('product_detail', args=[self.product.slug]))
        self.assertContains(response, 'Test description')

    def test_add_to_cart(self):
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]), {'quantity': 2})
        self.assertEqual(response.status_code, 302)
        cart = self.client.session['cart']
        self.assertEqual(int(cart[str(self.product.id)]), 2)
