import re
from .models import Restaurant, UserRestaurantRating
from .serializers import UserSerializer, RestaurantSerializer, UserRestaurantSerializer, TokenSerializr, RestaurantSerializerWithAvg
from rest_framework import serializers, status
from rest_framework.decorators import api_view, parser_classes, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Permission, User
from django.contrib.auth import authenticate
from django.db.models import Avg
from django.db.models.functions import Coalesce
from rest_framework.parsers import MultiPartParser, FormParser

@api_view(["POST"])
@permission_classes((AllowAny,))
def create_user_view(request):
    return create_user(request.data)

def create_user(data):
    if data:
        user_data = data
        user_object = User.objects.filter(username=user_data["username"])
        if user_object:
            error = {"detail": "User Already Exist"}
            return Response(error, status=status.HTTP_409_CONFLICT)

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            qs = User.objects.create(**serializer_data)
            qs.set_password(user_data["password"])
            qs.save()
            token = Token.objects.create(user=qs)
            serializer = TokenSerializr(token)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Please check your inputs"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Not Found"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((AllowAny,))
def login_view(request):
    user_data = request.data
    user_qs = authenticate(username=user_data["username"], password=user_data["password"])
    if user_qs:
        try:
            token = Token.objects.get(user=user_qs)
            print("test")
            serializer = TokenSerializr(token)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Error Authentication"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({"detail": "Unknown user"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_restaurant_list(request):
    if not request.user.is_superuser:
        qs = Restaurant.objects.all().annotate(avg=Coalesce(Avg("user_rating__rating"), 0.0)).order_by("-avg")
        serializer = RestaurantSerializerWithAvg(qs, many=True)
    else:
        qs = Restaurant.objects.all()
        serializer = RestaurantSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_restaurant_comments(request, id):
    qs = UserRestaurantRating.objects.filter(restaurant=id)
    serializer = UserRestaurantSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_user_restaurant_rating(request):
    return create_review(request.data)


def create_review(data):
    user_data = data
    if user_data:
        user = User.objects.filter(id=user_data["user"])
        restaurant = Restaurant.objects.filter(id=user_data["restaurant"])
        if user and restaurant:
            qs = UserRestaurantRating.objects.create(
                rating=user_data["rating"],
                comment=user_data["comment"],
                user=user[0],
                date=user_data["date"],
                restaurant=restaurant[0]
            )
            serializer = UserRestaurantSerializer(qs)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "data is missing"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "data is missing"}, status=status.HTTP_400_BAD_REQUEST)




###### Admin Operations #######

@api_view(["POST"])
@permission_classes([IsAdminUser])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
@parser_classes([MultiPartParser, FormParser])
def restaurants(request):
    user_data = request.data
    if user_data:
        serializer = RestaurantSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "please check your inputs"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Not Found"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET","DELETE","PUT"])
@permission_classes([IsAdminUser])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def restaurants_details(request, id):
    try:
        restaurant = Restaurant.objects.get(id=id)
    except Restaurant.DoesNotExist:
        return Response({"detail":"Restaurant does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = RestaurantSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Please check your inputs"}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        restaurant.delete()
        return Response({"detail":"Restaurant deleted Successfully"}, status=status.HTTP_200_OK)
    else:
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAdminUser])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def users(request):
    qs = User.objects.all().exclude(id=request.user.id)
    serializer = UserSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET","DELETE","PUT"])
@permission_classes([IsAdminUser])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def users_details(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"detail":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        if request.data["first_name"]:
            user.first_name = request.data["first_name"]
        if request.data["last_name"]:
            user.last_name = request.data["last_name"]
        if request.data["email"]:
            user.email = request.data["email"]

        if request.data["is_superuser"] != None:
            print(request.data["is_superuser"])
            user.is_superuser = request.data["is_superuser"]
        if request.data["is_staff"] != None:
            print(request.data["is_staff"])
            user.is_staff = request.data["is_staff"]
        
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        user.delete()
        return Response({"detail":"User deleted Successfully"}, status=status.HTTP_200_OK)
    else:
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET","POST"])
@permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def user_ratings(request):
    if request.method == "GET":
        qs = UserRestaurantRating.objects.all()
        serializer = UserRestaurantSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return create_review(request.data)



@api_view(["GET","DELETE","PUT"])
@permission_classes([IsAdminUser])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def user_ratings_details(request, id):

    try:
        userrestaurantrating = UserRestaurantRating.objects.get(id=id)
    except UserRestaurantRating.DoesNotExist:
        return Response({"detail":"Review does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        if request.data["rating"]:
            userrestaurantrating.rating = request.data["rating"]
        if request.data["comment"]:
            userrestaurantrating.comment = request.data["comment"]
        if request.data["date"]:
            userrestaurantrating.date = request.data["date"]
        userrestaurantrating.save()
        serializers = UserRestaurantSerializer(userrestaurantrating)
        return Response(serializers.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        userrestaurantrating.delete()
        return Response({"detail":"Record deleted Successfully"}, status=status.HTTP_200_OK)
    else:
        serializers = UserRestaurantSerializer(userrestaurantrating)
        return Response(serializers.data, status=status.HTTP_200_OK) 