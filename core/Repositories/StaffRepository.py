from authentication.models import User
from core.Repositories.Interfaces.IStaffRepository import OwnerRepository
from staff.models import Staff
from stores.models import Store
   

class OwnerRepositoryImpl(OwnerRepository):
    def is_owner_of_store(self, user_id: int, store_id: int) -> bool:
        try:
            store = Store.objects.get(id=store_id)
            return store.owner_id == user_id
        except Store.DoesNotExist:
            return False