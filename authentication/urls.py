from django.urls import path
from.views import (RegisterView,verifyEmail)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify/', verifyEmail.as_view(), name="email-verify"),
]

