from rest_framework import serializers
from backend.models import StoreOwners
from django.core.mail import send_mail
from django.conf import settings
class StoreOwnersSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    class Meta:
        model = StoreOwners
        fields = ['username','email', 'phone', 'firstname', 'lastname', 'date_of_birth', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = StoreOwners.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            phone=validated_data['phone'],
            date_of_birth=validated_data['date_of_birth']
        )
        
        return user