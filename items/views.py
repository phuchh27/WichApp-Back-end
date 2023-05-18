from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView

from items import permissions
from stores.models import Store
from .models import Item
from .serializers import ItemSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework import status


class ItemListCreateAPIView(ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsOwner,)

    def perform_create(self, serializer):
        store_id = self.kwargs.get('store_id')
        store = get_object_or_404(Store, id=store_id)
        if store.owner != self.request.user:
            return HttpResponseBadRequest('Invalid user')
        else:
            serializer.save(store_id=store_id)
            return JsonResponse({'message': 'Item created successfully'})
    def get_queryset(self):
        store_id = self.kwargs.get('store_id')
        store = get_object_or_404(Store, id=store_id)
        if store.owner == self.request.user:
            return Item.objects.filter(store_id=store_id)
        else:
            return Item.objects.none()