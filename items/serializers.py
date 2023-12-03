from django.shortcuts import get_object_or_404
from rest_framework import serializers

from stores.models import Store
from .models import Item , ItemCategory

class ItemSerializer(serializers.ModelSerializer):
    image = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = Item
        fields = ['category','id','name','code','description','cost','price','quantity','image', 'image_link']
    def validate(self, attrs):
        store_id = self.context['view'].kwargs.get('store_id')
        store = get_object_or_404(Store, id=store_id)
        if store.owner != self.context['request'].user:
            raise serializers.ValidationError('Invalid user')
        return attrs
    
class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta: 
        model = ItemCategory
        fields= '__all__'
    
    def validate(self, attrs):
        store_id = self.context['view'].kwargs.get('store_id')
        store = get_object_or_404(Store, id=store_id)
        if store.owner != self.context['request'].user:
            raise serializers.ValidationError('Invalid user')
        return attrs
    
class SelectItemByCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id','name','code','description','cost','price','quantity','image_link']


class ItemSocketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class UpdateItemSerializer(serializers.ModelSerializer):
    image = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Item
        fields = ['id','name','code','description','cost','price','quantity','image']

class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ['id', 'name', 'store']