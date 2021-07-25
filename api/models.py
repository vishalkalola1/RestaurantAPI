from django.db import models
from django.contrib.auth.models import User

# Create your models here.

RATING_CHOICES = ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5))


class Restaurant(models.Model):
    name = models.CharField(max_length=255, default="")
    address = models.CharField(max_length=255, default="")
    contact = models.CharField(max_length=20, default="")

    def __str__(self):
        return f"{self.name}"


class UserRestaurantRating(models.Model):
    rating = models.IntegerField(choices=RATING_CHOICES, default=0)
    comment = models.TextField(max_length=500, default="")
    date = models.PositiveBigIntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="user_rating")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.comment}"
