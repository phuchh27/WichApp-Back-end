# import from django library
from django.shortcuts import render
from django.contrib.sites.shortcuts import  get_current_site
from django.urls import reverse
from django.conf import settings
import redis
#import rest_framework library
from rest_framework import generics,status,views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import jwt

from authentication.services import get_store_id_by_user
#import inside project
from .serializers import LoginStaffSerializer, RegisterSerializer , EmailVerificationSerializer ,LoginSerializer,LogoutSerializer
from.models import User
from .utils import Util

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from urllib.parse import unquote
from rest_framework import permissions

from rest_framework.views import APIView
import json
# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self,request):
        user = request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username+' Use link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,'email_subject': 'Verify your email'}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)

class verifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    
    token_param_config = openapi.Parameter( 'token', 
                                           in_=openapi.IN_QUERY, 
                                           description='Description', 
                                           type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(
        manual_parameters=[token_param_config]
    )
    def get (self,request):
        token = request.GET.get('token')
        token = unquote(token)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email':'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LoginStaffAPIView(generics.GenericAPIView):
    serializer_class = LoginStaffSerializer
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogOutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

class onlineStaffsAPIView(APIView):
    def get(self, request):
        user = self.request.user.id
        user_store_id = get_store_id_by_user(user)

        redis_client = redis.Redis()
        all_keys = redis_client.keys("staff:*")

        matching_keys = [key.decode(
            "utf-8") for key in all_keys if f'StoreId_{user_store_id}' in key.decode("utf-8")]
        print(matching_keys)

        staffs = []
        for key in matching_keys:
            staff_json = redis_client.get(key)
            if staff_json is not None:
                id_part = key.split(':')[1]
                staff = json.loads(staff_json)
                staff['id'] = id_part
                staffs.append(staff)
        
        return Response(staffs, status=status.HTTP_200_OK)
