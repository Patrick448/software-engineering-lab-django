from datetime import datetime

from django.core.management.base import BaseCommand
from ...models import Product, Customer, Order


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        product1 = Product.objects.create(
        name='Juice',
        price=19.99,
        available=True
        )

        product2 = Product.objects.create(
            name='Water',
            price=9.99,
            available=False
        )

        product3 = Product.objects.create(
            name='Soda',
            price=14.99,
            available=True
        )

        customer1 = Customer.objects.create(
        name='John',
        address='Street 1'
        )

        customer2 = Customer.objects.create(
        name='Maria',
        address='Street 2'
        )

        order1 = Order.objects.create(
        customer=customer1,
        status='Sent',
        date=datetime.now()
        )

        order2 = Order.objects.create(
        customer=customer2,
        status='Completed',
        date=datetime.now()
        )
        order1.products.add(product1)
        order1.products.add(product2)
        order1.products.add(product3)

        order2.products.add(product1)
        order2.products.add(product3)

        self.stdout.write("Data created successfully.")

