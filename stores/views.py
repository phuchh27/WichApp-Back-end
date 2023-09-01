from django.shortcuts import render

#import from rest_framework
from rest_framework.generics import ListCreateAPIView ,RetrieveUpdateDestroyAPIView, RetrieveAPIView , ListAPIView, CreateAPIView
from rest_framework import permissions
from rest_framework.response import Response
from items.views import ItemListCreateAPIView
from rest_framework import status

from .serializers import StoreSerializer, categoriesSerializer
from .models import Category, Store

# Create store views
class storeListAPIView(ListAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Chỉ trị về các cửa hàng của nguồn ĳng nhỏ
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
        if count_of_stores >= 1:
            return Response(
                {"detail": "You already have a store. You need to pay a cost to create a new store.", "status": 402},
                status=status.HTTP_402_PAYMENT_REQUIRED
            )
        else:
            serializer.save(owner=self.request.user)
            return Response({"detail": "Store created successfully."}, status=status.HTTP_201_CREATED)


class StoresPayAPIView(CreateAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Chỉ trả về các cửa hàng của người dùng đăng nhập
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Gán owner là người dùng đăng nhập
        if not self.request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=403)
        elif self.request.user.is_staff:
            return Response({"detail": "You do not have permission to create a store."}, status=403)
        else:
            serializer.save(owner=self.request.user)
            return Response({"detail": "Store created successfully."}, status=201)

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
    