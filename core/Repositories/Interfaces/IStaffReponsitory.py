from typing import List
from authentication.models import User

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