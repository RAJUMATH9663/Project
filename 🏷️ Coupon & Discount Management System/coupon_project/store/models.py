from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name


class Coupon(models.Model):
    code = models.CharField(max_length=50)
    discount = models.IntegerField()  # percentage
    expiry = models.DateField()

    def is_valid(self):
        return self.expiry >= timezone.now().date()

    def __str__(self):
        return self.code