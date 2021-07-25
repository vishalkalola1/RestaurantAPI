from django.urls import path
from .views import (
    create_user_view,
    login_view,
    get_restaurant_list,
    get_restaurant_detail,
    create_user_restaurant_rating,
    restaurants,
    restaurants_details,
    users,
    users_details,
    user_ratings,
    user_ratings_details
)

urlpatterns = [
    path("register", create_user_view, name="register"),
    path("restaurants", get_restaurant_list, name="user-restaurants"),
    path("login", login_view, name="login"),
    path("restaurants/<int:id>", get_restaurant_detail, name="restaurnat-detail"),
    path("comment", create_user_restaurant_rating, name="create-comment"),

    #admin Urls
    path("admin/restaurants", restaurants, name="admin-restaurants"),
    path("admin/restaurants/<int:id>", restaurants_details, name="put-restaurant"),
    path("admin/users", users, name="users"),
    path("admin/users/<int:id>", users_details, name="user_details"),
    path("admin/reviews", user_ratings, name="users_reviews"),
    path("admin/reviews/<int:id>", user_ratings_details, name="users_reviews_details"),
]
