from datetime import datetime 
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken , TokenError

from authentication.services import get_store_id_by_user
from.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
import json
import redis

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    
    class Meta:
        model=User
        fields = ['email','username','password','phone']
        
    def validate(self,attrs):
        email = attrs.get('email','')
        username = attrs.get('username','')
        phone = attrs.get('phone','')
        
        if not username.isalnum():
            raise serializers.ValidationError('the username should only contain alphabetic characters')
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    class Meta:
        model = User
        fields = ['token']
        
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6,read_only=True)
    expiresIn = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_owner = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = ['email','password','username','tokens','id', 'expiresIn', 'is_staff','is_owner']
        
    def get_expiresIn(self):
        return int(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds())
    
    def validate(self,attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        user = auth.authenticate(email=email, password=password)
        filtered_user_by_email = User.objects.filter(email=email)

        if filtered_user_by_email[0].auth_provider !='email':
            raise AuthenticationFailed( detail='Please countrinue your login using, try again' + filtered_user_by_email[0].auth_provider)
        
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact the administrator')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        
        return {
            'id':user.id,
            'email':user.email,
            'username':user.username,
            'tokens':user.tokens,
            'expiresIn':self.get_expiresIn(),
            'is_staff':user.is_staff,
            'is_owner':user.is_owner

        }
        
        return super().validate(attrs)
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    default_error_messages={
        'bad_token':'Token is invalid or expired'
    }

    def validate(self,attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class LoginStaffSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)
    expiresIn = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_owner = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens', 'id', 'expiresIn', 'is_staff', 'is_owner']
        
    def get_expiresIn(self):
        return int(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds())
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        filtered_user_by_email = User.objects.filter(email=email)

        if filtered_user_by_email and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(detail='Please continue your login using, try again' + filtered_user_by_email[0].auth_provider)
        
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact the administrator')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        
        user_data = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'logintime': datetime.now().isoformat(),
        }
        store = get_store_id_by_user(user.id)
        redis_client = redis.Redis()
        redis_client.set(f'staff:{user.id}_StoreId_{store}', json.dumps(user_data))
        redis_client.expire(f'staff:{user.id}_StoreId_{store}', 28800)
        return user_data