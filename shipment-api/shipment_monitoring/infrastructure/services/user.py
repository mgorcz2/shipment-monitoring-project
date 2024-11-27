from shipment_monitoring.core.domain.user import User
from shipment_monitoring.infrastructure.dto.user import UserDTO
from shipment_monitoring.infrastructure.services.iuser import IUserService
from shipment_monitoring.core.repositories.iuser import IUserRepository
from shipment_monitoring.api.utils import consts
from shipment_monitoring.core.domain.user import UserIn
from shipment_monitoring.api.utils.token import TokenDTO
from shipment_monitoring.api.utils.token import create_access_token
from datetime import datetime, timedelta
from shipment_monitoring.api.utils import password_hashing

from uuid import UUID

class UserService(IUserService):
    _repository: IUserRepository

    def __init__(self, repository: IUserRepository):
        self._repository = repository

    async def register_user(self, user: UserIn) -> UserDTO | None:
        existing_user = await self._repository.get_user_by_username(user.username)
        if existing_user:
            raise ValueError("Username already registered")
        if user.role not in consts.ROLES:
            raise ValueError("invalid role")
        
        user.password = password_hashing.hash_password(user.password)
        return await self._repository.register_user(user)

    async def get_user_by_id(self, user_id:UUID) -> UserDTO | None:
        return await self._repository.get_user_by_id(user_id)
    
    async def get_user_by_username(self,username) -> User | None:
        return await self._repository.get_user_by_username(username)

    async def login_for_access_token(self, username, password) -> TokenDTO | None:
        user = await self._repository.get_user_by_username(username=username)
        if not user or not password_hashing.verify_password(password, user.password):
            raise ValueError("Incorrect username or password")
        access_token_expires = timedelta(minutes=consts.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}  
            