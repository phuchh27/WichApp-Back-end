from django.urls import path
from .views import RegisterView, verifyEmail, LoginAPIView,LogOutAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logOut/", LogOutAPIView.as_view(), name="logout"),
    path("email-verify/", verifyEmail.as_view(), name="email-verify"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
