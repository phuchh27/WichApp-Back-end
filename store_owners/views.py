
from rest_framework import status,generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
#from api.mixins import (StaffEditorPermissionMixin,UserQuerysetMixin)

from backend.models import StoreOwners
from .serializers import StoreOwnersSerializer
from django.core.mail import send_mail
from .utils import Utils


class StoreOwnersRegisterAPIView(generics.ListCreateAPIView):
    queryset = StoreOwners.objects.all()
    serializer_class = StoreOwnersSerializer
    def register_store_owner(self,request):
        owner = request.data
        serializer = self.serializer_class(data= owner)
        if serializer.is_valid():
            serializer.save()
            owner_data = serializer.data
            owner = StoreOwners.objects.get(email=owner_data['email'])
            token = RefreshToken.for_user(owner).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            
            absurl = "http://" + current_site + relativeLink + "?token" + str(token)
            
            email_body = 'Hi' + owner.username + 'Use link below to verify your account\n'+ absurl
            data = {'email_body': email_body,
                    'to_email': owner.email, 
                    'email_subject': 'Verify your email address'}
            Utils.send_email(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
store_owners_register_view = StoreOwnersRegisterAPIView.as_view()

class VerifyEmail(generics.GenericAPIView):
    def activate(self):
        pass
verify_email_view = VerifyEmail.as_view()