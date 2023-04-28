from rest_framework import serializers
from backend.models import StoreOwners

class StoreOwnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreOwners
        fields = ['email', 'phone', 'name', 'date_of_birth', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = StoreOwners.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            phone=validated_data['phone'],
            date_of_birth=validated_data['date_of_birth']
        )
        user.is_active = False  # set is_active to False
        user.save()
        return user