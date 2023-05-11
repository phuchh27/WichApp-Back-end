from django.shortcuts import render

#import from rest_framework
from rest_framework.generics import ListCreateAPIView ,RetrieveUpdateDestroyAPIView
from rest_framework import permissions

from items.views import ItemListCreateAPIView

from .serializers import StoreSerializer
from .models import Store
from .permissions import IsOwner
# Create store views
class StoresAPIView(ListCreateAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    permission = (permissions.IsAuthenticated,)
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class StoreDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = StoreSerializer
    permission = (permissions.IsAuthenticated,IsOwner,)
    queryset = Store.objects.all()
    lookup_field = "id"
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)  
     