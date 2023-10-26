
from django.urls import path
from .views import BillCreateAPIView

urlpatterns = [
    path('createBill/', BillCreateAPIView.as_view(), name='create_bill_into_redis_api'),
]