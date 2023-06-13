from django.db import models

from authentication.models import User
from stores.models import Store

# Create your models here.


class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
