from django.shortcuts import render
from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from stores.models import Store
from .serializers import RegisterStaffSerializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class StaffRegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterStaffSerializer
    permission_classes = [IsAuthenticated]