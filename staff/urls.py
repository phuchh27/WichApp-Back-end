from django.urls import path

from staff.views import StaffRegisterAPIView , StaffListView ,GetStoreIdAPIView

urlpatterns = [
    path('<int:store_id>/staff-register/', StaffRegisterAPIView.as_view(), name='staff-register'),
    path('<int:store_id>/', StaffListView.as_view(), name='staff-list'),
    path('get-store/', GetStoreIdAPIView.as_view(), name='get_store_id'),
    ]