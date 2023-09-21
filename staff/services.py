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