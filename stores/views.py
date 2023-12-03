from django.shortcuts import render

#import from rest_framework
from rest_framework.generics import ListCreateAPIView ,RetrieveUpdateDestroyAPIView, RetrieveAPIView , ListAPIView, CreateAPIView
from rest_framework import permissions
from rest_framework.response import Response
from items.views import ItemListCreateAPIView
from rest_framework import status

from .serializers import StoreSerializer, categoriesSerializer , StorePaidSerializer
from .models import Category, Store

from payment.services import create_payment_session , block_session

# Create store views
class storeListAPIView(ListAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
       
        return self.queryset.filter(owner=self.request.user)
    
class StoresAPIView(CreateAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        count_of_stores = Store.objects.filter(owner=self.request.user).count()

        if not self.request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)
        elif self.request.user.is_staff:
            return Response({"detail": "You do not have permission to create a store."}, status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():  # Check if the serializer data is valid
            if count_of_stores >= 1:
                payment_link = create_payment_session(self.request.user)
                return Response(
                    {"detail": "You already have a store. You need to pay a cost to create a new store.", "status": 402,"payment_link": payment_link},
                    status=status.HTTP_200_OK
                )
            else:
                serializer.save(owner=self.request.user)
                return Response({"detail": "Store created successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoresPayAPIView(CreateAPIView):
    serializer_class = StorePaidSerializer
    queryset = Store.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Chỉ trả về các cửa hàng của người dùng đăng nhập
        return self.queryset.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data, context={'request': request})
        # Gán owner là người dùng đăng nhập
        if not self.request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=403)
        elif self.request.user.is_staff:
            return Response({"detail": "You do not have permission to create a store."}, status=403)
        
        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user
            self.perform_create(serializer)
            # block_session(serializer.validated_data['verify_code'])
            return Response({"detail": "Store created successfully."}, status=201)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoreDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = StoreSerializer
    permission = (permissions.IsAuthenticated)
    queryset = Store.objects.all()
    lookup_field = "id"
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)  
    
class StoreItemAPIView(RetrieveAPIView):
    serializer_class = StoreSerializer
    permission = (permissions.IsAuthenticated)
    queryset = Store.objects.all()
    lookup_field = "id"
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
class CategoriesAPIView(ListAPIView):
    serializer_class = categoriesSerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    