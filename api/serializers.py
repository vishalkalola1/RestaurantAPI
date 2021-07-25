from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Restaurant, UserRestaurantRating


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "is_superuser",
            "is_staff",
            "id",
        )


class RestaurantSerializerWithAvg(serializers.ModelSerializer):
    avg = serializers.FloatField()

    class Meta:
        model = Restaurant
        fields = "__all__"

class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = "__all__"


class UserRestaurantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserRestaurantRating
        fields = "__all__"

class TokenSerializr(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Token
        fields = "__all__"
