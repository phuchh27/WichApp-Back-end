from django.urls import path
from .views import RegisterView, onlineStaffsAPIView, verifyEmail, LoginAPIView,LogOutAPIView,LoginStaffAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("loginstaff/", LoginStaffAPIView.as_view(), name="login"),
    path("logout/", LogOutAPIView.as_view(), name="logout"),
    path("email-verify/", verifyEmail.as_view(), name="email-verify"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("onlineStaffs", onlineStaffsAPIView.as_view(), name="online_staffs"),
]
