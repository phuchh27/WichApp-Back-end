#create url

from django.urls import path

from . import views

urlpatterns = [
    path('', views.StripeWebhookViewSet.as_view(), name = 'Read'),
]


