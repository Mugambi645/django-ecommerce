from importlib import import_module

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse

from store.models import Category, Product
from store.views import product_all


class TestViewResponses(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='admin')
        self.category = Category.objects.create(name='django', slug='django')
        self.product = Product.objects.create(
            category=self.category,
            title='django beginners',
            created_by=self.user,
            slug='django-beginners',
            price='20.00',
            image='django'
        )

    def test_url_allowed_hosts(self):
        """
        Ensure requests from disallowed and allowed hosts behave correctly.
        """
        response = self.client.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/', HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)

    def test_homepage_url(self):
        """
        Ensure the homepage URL returns HTTP 200 (OK).
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_list_url(self):
        """
        Ensure the category page returns HTTP 200 (OK).
        """
        response = self.client.get(
            reverse('store:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        Ensure the product detail page returns HTTP 200 (OK).
        """
        response = self.client.get(
            reverse('store:product_detail', args=['django-beginners']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """
        Validate homepage HTML contains expected title text.
        """
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()

        response = product_all(request)
        html = response.content.decode('utf8')

        self.assertIn('BookStore', html)
        self.assertEqual(response.status_code, 200)
