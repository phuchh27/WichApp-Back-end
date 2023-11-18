# urls.py
from django.urls import path
from .views import GoogleSocialAuthView

urlpatterns = [
    # Your existing URLs
    path('google-auth/', GoogleSocialAuthView.as_view(), name='google-social-auth'),
]
