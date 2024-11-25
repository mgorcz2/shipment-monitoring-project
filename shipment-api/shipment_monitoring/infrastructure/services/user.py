from shipment_monitoring.core.domain.user import User
from shipment_monitoring.infrastructure.dto.user import UserDTO
from shipment_monitoring.infrastructure.services.iuser import IUserService
from shipment_monitoring.api.security import utils
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
async def hash_password(password) -> str:
    return pwd_context.hash(password)



class UserService(IUserService):
    _repository: IUserService

    def __init__(self, repository: IUserService):
        self._repository = repository

    async def register_user(self, user: UserDTO) -> UserDTO | None:
        existing_user = await self._repository.get_user_by_username(user.username)
        if existing_user:
            raise ValueError("Username already registered")
        if user.role not in utils.ROLES:
            raise ValueError("invalid role")
        
        user.password = await hash_password(user.password)
        return await self._repository.register_user(user)

    async def get_user_by_id(self, user_id) -> UserDTO | None:
        return await self._repository.get_user_by_id(user_id)
    
    async def get_user_by_username(self,username) -> UserDTO | None:
        return await self._repository.get_user_by_username(username)
