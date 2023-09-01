from django.db import models
from authentication.models import User
# Create your models here.

class PaymentSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # If you want to associate the session with a user
    session_id = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

def __str__(self):
        return f"PaymentSession for User: {self.user.username}"