from django.urls import path
from .views import (
    create_user_view,
    login_view,
    get_restaurant_list,
    get_restaurant_detail,
    create_user_restaurant_rating,
)

urlpatterns = [
    path("register", create_user_view, name="register"),
    path("restaurants", get_restaurant_list),
    path("login", login_view, name="login"),
    path("restaurants/<int:id>", get_restaurant_detail, name="restaurnat-detail"),
    path("comment", create_user_restaurant_rating, name="create-comment"),
]
