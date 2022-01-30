from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    rating = models.FloatField()

class RestaurantSystemUser(models.Model):
    user = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    restaurant = models.TextField(blank=True, null=True)
