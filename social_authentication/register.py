import json
from typing import Self
from django.contrib import auth
from requests import request
from authentication.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)

def get_expiresIn(self):
        return int(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds())

def register_social_user(provider, user_id, email, name, exp):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:
            password = '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'
            user = auth.authenticate(request, email=email, password=password)

            if user is not None:
                tokens_dict =  user.tokens()
                tokens = json.dumps(tokens_dict)
                return {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'tokens': tokens,
                    'expiresIn': exp,
                    'is_staff': user.is_staff,
                    'is_owner': user.is_owner
                }
            else:
                try:
                    user_by_email = User.objects.get(email=email)
                    return {'error': 'Incorrect password for the provided email'}
                except User.DoesNotExist:
                    return {'error': 'No user found with the provided email'}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'username': generate_username(name), 'email': email,
            'password': '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'}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.is_active = True
        user.is_staff = False
        user.is_owner = True
        user.auth_provider = provider

        # Set a local password for the user
        user.set_password('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')
        user.save()

        new_user = auth.authenticate(
            email=email, password='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')
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens()
        }
