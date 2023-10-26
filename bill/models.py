import random
import string
from django.db import models
from django.core.validators import MinValueValidator

from stores.models import Store
from authentication.models import User
from items.models import Item




# Create your models here.

def generate_random_id():
    """Generate a random 10-digit alphanumeric ID."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

class Bill(models.Model):
    id = models.CharField(max_length=10, primary_key=True, default=generate_random_id)
    date_create = models.DateTimeField(auto_now_add=True)
    date_paid = models.DateTimeField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bill {self.id} - Store {self.store_code} - Employee {self.employee_code}"

class BillDetail(models.Model):
    bill = models.ForeignKey('Bill', related_name='bill_details', on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"Bill {self.bill.id} - Product {self.product.product_code} - Quantity {self.quantity}"