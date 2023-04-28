
import secrets
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
class MyUserManager(BaseUserManager):
        
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class StoreOwners(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    objects = MyUserManager()

class Store(models.Model):
    store_code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(StoreOwners, on_delete=models.CASCADE)

class Employee(models.Model):
    name = models.CharField(max_length=255)
    card_id = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    cost_in_hour = models.FloatField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

class Product(models.Model):
    name = models.CharField(max_length=255)
    cost = models.FloatField()
    price = models.FloatField()
    description = models.TextField()
    quantity = models.IntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
