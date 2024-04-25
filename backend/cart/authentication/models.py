from django.db import models
from django.contrib.auth import get_user_model

class Cart(models.Model):
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user_id = models.IntegerField(default=1)
    product_id = models.IntegerField(default=2) # Assuming this is the field for product ID
    brand = models.CharField(max_length=100,default='Default Brand')
    name = models.CharField(max_length=100, default='Default Name')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def item_total(self):
        return self.quantity * self.total_price

    def __str__(self):
        return f"Cart item - Quantity: {self.quantity}, Total Price: {self.total_price}"


class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} - {self.zipcode}"
