from .models import Restaurant, UserRestaurantRating
from .serializers import (
    UserSerializer,
    RestaurantSerializer,
    UserRestaurantSerializer,
    TokenSerializr,
)

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Avg
from django.db.models.functions import Coalesce
from datetime import datetime

# Create your views here.


@api_view(["POST"])
@permission_classes((AllowAny,))
def create_user_view(request):
    if request.data:
        user_data = request.data
        user_object = User.objects.filter(username=user_data["username"])
        if user_object:
            return Response(
                {"detail": "User Already Exist"}, status=status.HTTP_409_CONFLICT
            )

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer_data = serializer.validated_data
            qs = User.objects.create(**serializer_data)
            qs.set_password(user_data["password"])
            qs.save()

            token = Token.objects.get_or_create(
                user_id=User.objects.get_or_create(
                    username=serializer.data["username"]
                )[0].id
            )
            serializer = TokenSerializr(token[0])

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"detail": "please check your inputs"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    return Response({"detail": "Not Found"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_restaurant_list(request):

    qs = (
        Restaurant.objects.all()
        .annotate(avg=Coalesce(Avg("user_rating__rating"), 0.0))
        .order_by("-avg")
    )
    serializer = RestaurantSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_restaurant_detail(request, id):
    qs = UserRestaurantRating.objects.filter(restaurant=id)
    serializer = UserRestaurantSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes((AllowAny,))
def login_view(request):
    user_data = request.data
    user_qs = authenticate(
        username=user_data["username"], password=user_data["password"]
    )
    if user_qs:
        token = Token.objects.get(
            user=user_qs,
        )
        serializer = TokenSerializr(token)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        {"detail": "Authentication Error"}, status=status.HTTP_404_NOT_FOUND
    )



@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_user_restaurant_rating(request):
    user_data = request.data
    if user_data:
        qs = UserRestaurantRating.objects.create(
            rating=user_data["rating"],
            comment=user_data["comment"],
            user=User.objects.get(id=user_data["user"]),
            date=user_data["date"],
            restaurant=Restaurant.objects.get(id=user_data["restaurant"]),
        )
        serializer = UserRestaurantSerializer(qs)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({"detail": "data is missing"}, status=status.HTTP_400_BAD_REQUEST)
