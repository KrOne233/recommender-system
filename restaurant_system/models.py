import pandas as pd
from django.db import models


class Restaurant(models.Model):
#    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'restaurant'



class Restaurantsystemuser(models.Model):
    #    id = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=200, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    restaurant = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'restaurantsystemuser'
