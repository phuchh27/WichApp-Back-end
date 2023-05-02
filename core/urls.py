
from django.contrib import admin
from django.urls import path
from backend.views import HelloWorld
from store_owners.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('hello/', HelloWorld.as_view(), name='hello'),
    path('register/', store_owners_register_view, name='register_store_owner'),
    path('email-verify/', verify_email_view, name='email-verify'),
    
]
