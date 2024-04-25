from django.db import models

class Watch(models.Model):
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    more_description = models.TextField()
    rating = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.DateField()

    def __str__(self):
        return self.name
