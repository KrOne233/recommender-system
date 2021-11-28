from django.db import models

# Create your models here.
class Restaurant(models.Model):
    restaurantName = models.CharField(max_length = 50)
    restaurantAddress = models.CharField(max_length=100) 
