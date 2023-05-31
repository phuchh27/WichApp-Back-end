from authentication.models import User
from .Interfaces import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, context):
        self._context = context  
    
    def create_staff(self, user:User)-> bool:
        new_staff = User(
            username=user.username,
            
        )
        