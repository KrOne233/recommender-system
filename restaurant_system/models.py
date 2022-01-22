from django.db import models
# from django.db import connections

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    rating = models.FloatField()



class RestaurantSystemUser(models.Model):
    # id = models.IntegerField(blank=False, null=False)
    user = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    restaurant = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'restaurant_system_user'



  


     