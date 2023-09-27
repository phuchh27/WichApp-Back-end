from django.http import Http404, HttpResponseBadRequest, JsonResponse
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from items import permissions
from stores.models import Store
from .models import Item
from .serializers import ItemSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from utils.cloudinary import Cloudinary
import base64
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile


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
