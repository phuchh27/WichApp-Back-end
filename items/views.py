from django.http import Http404, HttpResponseBadRequest, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from items import permissions
from stores.models import Store
from .models import Item, ItemCategory
from .serializers import ItemCategorySerializer, ItemSerializer, SelectItemByCategorySerializer,ItemSocketSerializer,UpdateItemSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from utils.cloudinary import Cloudinary
import base64
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db.models import F
from .services import ItemService
from django.shortcuts import get_object_or_404


class ItemListCreateAPIView(ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsOwner,)
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        store_id = self.kwargs.get('store_id')
        image_base64 = self.request.data['image']
        serializer.validated_data.pop('image')
        name = self.request.data['name']
        code = self.request.data['code']
        cloudinary_service = Cloudinary()
        # print(image_base64)
        if image_base64:
            format,imgstr = image_base64.split(';base64,')
            ext = format.split('/')[-1]

            image_data = base64.b64decode(imgstr)

            # image = Image.open(BytesIO(image_data))

            image_url = cloudinary_service.upload_image(image_data, name, code)
            print(image_url, ' ok')
            serializer.save(store_id=store_id, image_link=image_url)
        else:
            image_url = 'https://res.cloudinary.com/dm4renyes/image/upload/v1695789028/empty-img_xqrhau.png'
            serializer.save(store_id=store_id, image_link=image_url)
    
    def get_queryset(self):
        store_id = self.kwargs.get('store_id')
        store = get_object_or_404(Store, id=store_id)
        if store.owner == self.request.user:
            return Item.objects.filter(store_id=store_id)
        else:
            return Item.objects.none()


class ItemUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = UpdateItemSerializer
    lookup_field = 'id'  # assuming you are passing 'item_id' in the URL path

    def perform_update(self, serializer):
        item_id = self.kwargs.get('id')

        image_base64 = self.request.data.get('image', None)

        if 'image' in self.request.data:
            serializer.validated_data.pop('image')

        name = self.request.data.get('name', serializer.instance.name)
        code = self.request.data.get('code', serializer.instance.code)
        cloudinary_service = Cloudinary()

        image_link = ItemService.get_image_link_by_item_id(item_id)
        store_id = ItemService.get_store_id_by_item_id(item_id)
        category_id = ItemService.get_category_id_by_item_id(item_id)

        if image_base64:
            try:
                format, imgstr = image_base64.split(';base64,')
                ext = format.split('/')[-1]
                image_data = base64.b64decode(imgstr)
            except Exception as e:
                return Response({'error': 'Invalid image data format'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                image_url = cloudinary_service.upload_image(image_data, name, code)
                # cloudinary_service.delete_image(image_link)

                serializer.validated_data.update({
                    'image_link': image_url,
                    'store_id': store_id,
                    'category_id': category_id
                })
                serializer.save()
            except Exception as e:
                return Response({'error': 'Error uploading image to Cloudinary'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            serializer.validated_data.update({
                'store_id': store_id,
                'category_id': category_id
            })
            serializer.save()
    

class ItemDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    lookup_field = "id"
    

    def get_queryset(self):
        store_id = self.kwargs.get('store_id')
        store = get_object_or_404(Store, id=store_id)
        permission_classes = (permissions.IsOwner,)
        if store.owner == self.request.user:
            return self.queryset.filter(store_id=store_id) 
        else:
            return Item.objects.none()

class ItemCategoryListCreateView(ListCreateAPIView):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer

class ItemCategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer

class SelectItemByCategoryAPIView(ListAPIView):
    serializer_class = SelectItemByCategorySerializer
    # permission_classes = (permissions.IsOwner)

    def get_queryset(self):
        store_id = self.kwargs['store_id']
        category_id = self.kwargs['category_id']
        queryset = Item.objects.filter(store_id=store_id, category_id=category_id)
        return queryset
    

class GetItemsByStoreId(ListAPIView):
    serializer_class = ItemSocketSerializer

    def get_queryset(self):
        store_id = self.kwargs['store_id']
        return Item.objects.filter(store_id=store_id)