from django.db import models
from authentication.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    
class Store(models.Model):
    shopname = models.CharField(max_length=255)
    description = models.TextField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default= True)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.FileField(upload_to='media', blank=True, null=True)
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.shopname



    
    