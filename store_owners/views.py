import secrets
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect

from backend.models import StoreOwners
from .serializers import StoreOwnersSerializer
from django.core.mail import send_mail
@api_view(['POST'])
def register_store_owner(request):
    serializer = StoreOwnersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
