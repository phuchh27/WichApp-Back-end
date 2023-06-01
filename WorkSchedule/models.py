
from datetime import datetime, timedelta
from django.db import models

from authentication.models import User
from stores.models import Store

# Create your models here.
class WorkSchedule (models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=250)
    start_day = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        self.end_day = self.start_day + timedelta(days=7)
        super().save(*args, **kwargs)
        
class S_WorkSchedule (models.Model):
    work_day = models.DateField()
    shift = models.CharField(max_length=20)
    description = models.TextField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['work_day', 'shift']

class O_WorkSchedule (models.Model):
    work_day = models.DateField()
    shift = models.CharField(max_length=20)
    description = models.TextField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE) 
    
