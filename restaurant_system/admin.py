from django.contrib import admin
from .models import Restaurant, RestaurantSystemUser


# Register your models here.
admin.site.register(Restaurant)
admin.site.register(RestaurantSystemUser)