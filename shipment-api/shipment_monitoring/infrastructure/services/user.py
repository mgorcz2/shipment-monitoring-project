from shipment_monitoring.core.domain.user import User
from shipment_monitoring.infrastructure.dto.user import UserDTO
from shipment_monitoring.infrastructure.services.iuser import IUserService


class UserService(IUserService):
    _repository: IUserService

    def __init__(self, repository: IUserService):
        self._repository = repository

    async def add_user(self, user: UserDTO) -> UserDTO | None:
        return await self._repository.add_user(user)

    async def get_user_by_id(self, user_id) -> UserDTO | None:
        return await self._repository.get_user_by_id(user_id)