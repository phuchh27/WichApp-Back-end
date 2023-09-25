from django.shortcuts import render
from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from authentication.models import User
from staff.services import list_staff, staff_info_list
from stores.models import Store
from stores.services import check_owmer
from .serializers import RegisterStaffSerializer, StaffsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


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
