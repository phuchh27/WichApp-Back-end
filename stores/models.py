from django.db import models
from authentication.models import User
# Create your models here.
class Store(models.Model):
    
    CATEGORY_OPTIONS =[
        ('FOOD','FOOD'),
        ('COFFEE','COFFEE'),
        ('FASHION','FASHION'),
        ('OTHER','OTHER')
    ]
    
    category = models.CharField(choices=CATEGORY_OPTIONS,max_length=255)
    shopname = models.CharField(max_length=255)
    description = models.TextField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default= True)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.FileField(upload_to='store_images', blank=True, null=True)
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE)
    
    
    