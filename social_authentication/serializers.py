import os

from social_authentication.register import register_social_user

from. import google

from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()


    def validate(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError('Invalid token. Please login again')
        
        if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):
            raise AuthenticationFailed('oops, who are you?')
        
        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider = provider, user_id = user_id, email = email, name = name
        )