from typing import List
from authentication.models import User
from abc import ABC, abstractmethod
class IStaffRepository:
    def  get(self, id: int) -> bool:
        pass

    def  get_all(self) -> List[User]:
        pass

    def  create_staff(self, user: User) -> bool:
        pass

    def  update_staff(self, user: User) -> bool:
        pass

    def  delete_staff(self, id: int) -> bool:
        pass 
    
    def is_staff_of_store(self, store_id: int, staff_id: int) -> bool:
        pass

class OwnerRepository(ABC):
    @abstractmethod
    def is_owner_of_store(self, user_id: int, store_id: int) -> bool:
        pass