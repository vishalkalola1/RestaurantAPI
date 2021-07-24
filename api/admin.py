from django.contrib import admin
from .models import Restaurant, UserRestaurantRating

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(UserRestaurantRating)
