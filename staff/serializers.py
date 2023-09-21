from rest_framework import serializers

from authentication.models import User
from staff.models import Staff
from stores.models import Store


class RegisterStaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password','phone']
        
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        store_id = self.context['view'].kwargs.get('store_id')
        
        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphabetic characters')
        
        try:
            store = Store.objects.get(id=store_id)
            if store.owner != self.context['request'].user:
                raise serializers.ValidationError('You are not the owner of this store')
        except Store.DoesNotExist:
            raise serializers.ValidationError('Invalid store_id')
        
        return attrs
    
    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)
        user.is_verified=True
        user.save()
        store_id = self.context['view'].kwargs.get('store_id')
        try:
            store = Store.objects.get(id=store_id)
            staff = Staff.objects.create(user_id=user.id, store_id=store.id)
        except Store.DoesNotExist:
            pass
        return user


class StaffsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email','phone','is_active')