from rest_framework import serializers
from .models import Category, Store
class StoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Store
        fields = ['id','shopname', 'description','phone','address','category','image_url' ]
    
    
class categoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']  

class StorePaidSerializer(serializers.ModelSerializer):
    verify_code = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = Store
        fields = ['id','shopname', 'description','phone','address','category','image_url','verify_code' ]