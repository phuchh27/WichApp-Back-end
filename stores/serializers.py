from rest_framework import serializers
from .models import Store
class StoreSerializer(serializers.ModelSerializer):
    create_new_item = serializers.SerializerMethodField()
    class Meta:
        model = Store
        fields = ['id','shopname', 'description','phone','address','category','create_new_item']
    
    def get_create_new_item(self, obj):
        return f"http://127.0.0.1:8000/stores/{int(obj.id)}/items"
    
    