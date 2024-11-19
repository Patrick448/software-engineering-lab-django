from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


def price_validator(val):
    if val < 0:
        raise ValidationError(f"Price {val} is negative")


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[price_validator])
    available = models.BooleanField()


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)


class Order(models.Model):
    STATUS_CHOICES = {
        'New': 'New',
        'In Process': 'In Process',
        'Sent': 'Sent',
        'Completed': 'Completed',
        }
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    date = models.DateField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)


    def get_total_price(self):
        sum = 0
        for product in self.products.related_model.all():
            sum += product.price

        return sum

    def check_order_possible(self):
        possible = True
        for product in self.products.related_model.all():
            if not product.available:
                possible = False
                break

        return possible


