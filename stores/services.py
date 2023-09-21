from .models import Store

def check_owmer(store_id , user):
    try: 
        store = Store.objects.get(id=store_id)
        return store.owner == user
    except Store.DoesNotExist:
        return False
    