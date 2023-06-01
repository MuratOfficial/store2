from http import HTTPStatus
from django.urls import reverse
from django.test import TestCase

from .models import Product, ProductCategory


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductListViewTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)
        products = Product.objects.all()

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
        # self.assertEquals(response.context_data['object_list'], products[:3])
# Create your tests here.

