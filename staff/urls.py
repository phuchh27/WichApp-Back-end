from django.urls import path

from staff.views import StaffRegisterAPIView

urlpatterns = [
    path('<int:store_id>/staff-register/', StaffRegisterAPIView.as_view(), name='staff-register'),
    ]