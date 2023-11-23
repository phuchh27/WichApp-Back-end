from django.http import JsonResponse
from .models import Staff
from authentication.models import User

def list_staff(store_id):
    staff_ids = Staff.objects.filter(store_id=store_id).values_list('user_id', flat=True)
    return staff_ids

def staff_info_list(user_ids):

    users = User.objects.filter(id__in=user_ids).values('username', 'email')

    data = list(users)
    print(data)
    return JsonResponse(data, safe=False)

def get_store_id(id):

    storeId = Staff.objects.get(user_id=id).store_id

    return JsonResponse(storeId, safe=False)

class StaffService:
    @staticmethod
    def get_staff_by_store_ids(store_ids, working_status=True):
        staff = Staff.objects.filter(store_id__in=store_ids,working_status = working_status)
        return staff
    
    @staticmethod
    def get_store_id_by_user_id(user_id):
        try:
            staff = Staff.objects.get(user_id=user_id)
            store_id = staff.store_id
            return store_id
        except Staff.DoesNotExist:
            return None