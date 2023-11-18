from .models import User
from staff.models import Staff
from items.models import Item


def is_user_staff(user_id):
    try:
        user = User.objects.get(pk=user_id)
        return user.is_staff
    except User.DoesNotExist:
        return False


def checkOwner(user_id):
    pass

def get_store_id_by_user(user_id):
    try:
        staff_instance = Staff.objects.get(user_id=user_id)
        return staff_instance.store_id
    except Staff.DoesNotExist:
        return None
    
def get_product_quntity(product_id):
    try:
        item_instance = Item.objects.get(pk=product_id)
        return item_instance.quantity
    except Item.DoesNotExist:
        return None
class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None