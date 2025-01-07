from django.db import DataError
from django.test import TestCase
from se_lab_app.models import Product, Customer, Order
from django.core.exceptions import ValidationError


class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name='Temporary customer', address='Temporary address')
        self.product = Product.objects.create(name='Temporary product', price=1.99, available=True)
        self.product2 = Product.objects.create(name='Temporary product 2', price=2.99, available=False)

    def test_create_order_with_valid_data(self):
        temp_order = Order.objects.create(customer=self.customer, date='2021-01-01', status='New')
        temp_order.products.add(self.product)
        self.assertEqual(temp_order.customer, self.customer)
        self.assertEqual(temp_order.date, '2021-01-01')
        self.assertEqual(temp_order.status, 'New')
        self.assertEqual(temp_order.products.all()[0], self.product)

    def test_create_order_with_missing_status(self):
        with self.assertRaises(ValidationError):
            temp_order = Order.objects.create(customer=self.customer, date='2021-01-01')
            temp_order.full_clean()

    def test_calculate_total_price(self):
        temp_order = Order.objects.create(customer=self.customer, date='2021-01-01', status='New')
        temp_order.products.add(self.product)
        temp_order.products.add(self.product2)
        self.assertEqual(float(temp_order.get_total_price()), 4.98)


    def test_calculate_total_price_no_products(self):
        temp_order = Order.objects.create(customer=self.customer, date='2021-01-01', status='New')
        self.assertEqual(float(temp_order.get_total_price()), 0)

    def test_check_order_possible_1(self):
        temp_order = Order.objects.create(customer=self.customer, date='2021-01-01', status='New')
        temp_order.products.add(self.product)
        self.assertTrue(temp_order.check_order_possible())

    def test_check_order_possible_2(self):
        temp_order = Order.objects.create(customer=self.customer, date='2021-01-01', status='New')
        temp_order.products.add(self.product)
        temp_order.products.add(self.product2)
        self.assertFalse(temp_order.check_order_possible())


class CustomerModelTest(TestCase):

    def test_create_customer_with_valid_data(self):
        temp_customer = Customer.objects.create(name='Temporary customer', address='Temporary address')
        self.assertEqual(temp_customer.name, 'Temporary customer')
        self.assertEqual(temp_customer.address, 'Temporary address')

    def test_create_customer_with_long_name_1(self):
        temp_customer = Customer.objects.create(name='a' * 100, address='Temporary address')
        self.assertTrue(temp_customer)

    def test_create_customer_with_long_name_2(self):
        with self.assertRaises(DataError):
            temp_customer = Customer.objects.create(name='a' * 101, address='Temporary address')
            temp_customer.full_clean()

    def test_create_customer_with_missing_name(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer.objects.create(address='Temporary address')
            temp_customer.full_clean()

class ProductModelTest(TestCase):
    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(name='Temporary product',
        price=1.99, available=True)
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Invalid product', price = "-1.99", available = True)
            temp_product.full_clean()

    def test_create_product_without_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(price = "1.99", available = True)
            temp_product.full_clean()

    def test_create_product_with_long_name_1(self):
        temp_product = Product.objects.create(name='a' * 255, price="1.99", available=True)
        self.assertTrue(temp_product.available)

    def test_create_product_with_long_name_2(self):
        with self.assertRaises(DataError):
            temp_product = Product.objects.create(name='a' * 256, price = "1.99", available = True)
            temp_product.full_clean()

    def test_create_product_with_price_many_decimal_places(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='test', price="1.992", available=True)
            temp_product.full_clean()


    def test_create_product_with_price_many_digits(self):
        with self.assertRaises(DataError):
            temp_product = Product.objects.create(name='test', price="123456789.99", available=True)
            temp_product.full_clean()
