from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from authentication.models import User
from authentication.services import UserService
from staff.models import Staff
from staff.services import StaffService, list_staff, staff_info_list
from stores.models import Store
from stores.services import StoreService, check_owmer
from .serializers import GetAllStaffSerializer, RegisterStaffSerializer, StaffsSerializer, StoreIdSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.views.decorators.http import require_POST


# Create your views here.
class StaffRegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterStaffSerializer
    permission_classes = [IsAuthenticated]

# class StaffListAPIView(generics.ListAPIView):

class StaffListView(generics.ListAPIView):
    serializer_class = StaffsSerializer

    def get_queryset(self):
        user_ids = list_staff(self.kwargs['store_id']) 
        return User.objects.filter(id__in=user_ids)
    

class GetStoreIdAPIView(APIView):
    def get(self, request):
        try:
            user_id = request.user.id
            staff_instance = Staff.objects.get(user_id=user_id)
            store_id = staff_instance.store_id

            # Create an instance of the serializer
            serializer = StoreIdSerializer({'store_id': store_id})

            return Response(serializer.data)
        except Staff.DoesNotExist:
            return Response({'error': 'Staff instance not found for the given user ID'}, status=status.HTTP_404_NOT_FOUND)
class StaffByOwnerIdAPIView(APIView):
    def get(self, request):
        
        owner_id = request.user.id
        store_ids = StoreService.get_store_ids_by_owner(owner_id)   
        staff_members = StaffService.get_staff_by_store_ids(store_ids)
        staff_details = []
        for staff in staff_members:
            user_id = staff.user.id
            user = UserService.get_user_by_id(user_id)

            if user:
                user_serializer = GetAllStaffSerializer(user).data
                staff_details.append(user_serializer)

        return Response(staff_details, status=status.HTTP_200_OK)