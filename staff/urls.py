from django.urls import path

from staff.views import RemoveStaffAPIView, StaffByOwnerIdAPIView, StaffRegisterAPIView, StaffListView, GetStoreIdAPIView, StaffUpdateAPIView

urlpatterns = [
    path('<int:store_id>/staff-register/',
         StaffRegisterAPIView.as_view(), name='staff-register'),
    path('<int:store_id>/', StaffListView.as_view(), name='staff-list'),
    path('get-store/', GetStoreIdAPIView.as_view(), name='get_store_id'),
    path('get/staff/owner/', StaffByOwnerIdAPIView.as_view(),
         name='staff-by-owner-id-api'),
    path('update/<int:staff_id>/', StaffUpdateAPIView.as_view(),
         name='update-staff-infomation'),
     path('remove/<int:staff_id>/', RemoveStaffAPIView.as_view(),
         name='remove-staff'),
]
