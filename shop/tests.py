import datetime
import random
import factory

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from .models import Product, Shop, Supplies, Sales


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    title = factory.Faker("name")
    description = factory.Faker("sentence")
    price = 100.00


class ShopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Shop
    title = factory.Faker("name")
    address = factory.Faker("sentence")


class SuppliesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplies

    product = factory.Iterator(Product.objects.all())
    shop = factory.Iterator(Shop.objects.all())
    date = datetime.datetime.now()
    quantity = random.randint(200, 20_000)


class SalesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sales

    product = factory.Iterator(Product.objects.all())
    shop = factory.Iterator(Shop.objects.all())
    date = datetime.datetime.now()
    quantity = random.randint(200, 20_000)


class ShopTest(APITestCase):
    def setUp(self):
        products = ProductFactory.create_batch(100)
        shops = ShopFactory.create_batch(10)
        supplies = SuppliesFactory.create_batch(30)
        sales = SalesFactory.create_batch(15)

    def test_objects_count(self):
        self.assertEqual(Product.objects.all().count(), 100)
        self.assertEqual(Shop.objects.all().count(), 10)
        self.assertEqual(Supplies.objects.all().count(), 30)
        self.assertEqual(Sales.objects.all().count(), 15)

    def test_create_product(self):
        url = reverse('add_product')
        data = {"title": "QWERTY",
                "description": "QWERTY",
                "price": 200.50}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_shop(self):
        url = 'https://127.0.0.1:8000/api/v1/stores/'
        data = {"title": "QWERTY",
                "address": "QWERTY"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_supplies(self):
        url = 'https://127.0.0.1:8000/api/v1/stores/3/supply/'
        data = [{"product": 7, "quantity": 100},
                {"product": 10, "quantity": 200}]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_sales(self):
        instance = Supplies.objects.get(id=1)
        url = f'https://127.0.0.1:8000/api/v1/stores/{instance.shop_id}/buy/'
        data = {"product": instance.product_id, "quantity": instance.quantity}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)