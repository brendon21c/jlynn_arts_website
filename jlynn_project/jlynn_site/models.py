from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
import PIL
from decimal import Decimal
# Create your models here.

class Art(models.Model):
    """Database containing all relevant information for artwork."""

    title = models.CharField(max_length=200, blank=False)
    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    media = models.TextField(max_length=1000, blank=False)
    status = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    photo_small = models.ImageField(upload_to='images/small/', blank=True)
    photo_large= models.ImageField(upload_to='images/large/', blank=True)
