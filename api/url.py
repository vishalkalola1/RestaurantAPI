from django.urls import path
from .views import (
    create_user_view,
    login_view,
    get_restaurant_list,
    get_restaurant_comments,
    restaurants,
    restaurants_details,
    users,
    users_details,
    user_ratings,
    user_ratings_details
)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("register", create_user_view, name="register"),
    path("login", login_view, name="login"),
    path("restaurants", get_restaurant_list, name="user-restaurants"),
    path("restaurants/<int:id>/reviews", get_restaurant_comments, name="restaurnat-comments"),
    # path("reviews", create_user_restaurant_rating, name="create-comment"),

    #admin Urls
    path("restaurants/create", restaurants, name="admin-restaurants"),
    path("restaurants/<int:id>", restaurants_details, name="put-restaurant"),
    path("users", users, name="users"),
    path("users/<int:id>", users_details, name="user_details"),
    path("reviews", user_ratings, name="users_reviews"),
    path("reviews/<int:id>", user_ratings_details, name="users_reviews_details"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
