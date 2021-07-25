from django.contrib import admin
from .models import Restaurant, UserRestaurantRating

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address','contact')

class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'rating', 'comment', 'date')

# Register your models here.
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(UserRestaurantRating, ReviewsAdmin)
