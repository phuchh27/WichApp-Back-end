from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
import os

from social_authentication.register import register_social_user

from . import google
import facebook


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        print(user_data)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is eithe invalid or has expired. Please login again')

        if user_data['aud'] != '50348836962-oa6k09cpohca4qvncnqh9m6k5h0k2uqd.apps.googleusercontent.com':
            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        exp = user_data['exp']
        provider = 'google'

        print(email)

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name , exp=exp
        )


class FacebookSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)
        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            return register_social_user(
                provider=provider, user_id=user_id, email=email, name=name
            )

        except Exception as identifier:
            raise serializers.ValidationError(
                'The token is eithe invalid or has expired. Please login again')

