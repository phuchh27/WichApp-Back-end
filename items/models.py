from django.db import models
from stores.models import Store
# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=0)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.IntegerField(default=0)
    store = models.ForeignKey(to=Store,on_delete=models.CASCADE)
