from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from src.infrastructure.repositories.shipmentdb import (
    ShipmentRepository,
)
from src.infrastructure.repositories.userdb import UserRepository
from src.infrastructure.services.shipment import ShipmentService
from src.infrastructure.services.user import UserService


class Container(DeclarativeContainer):
    shipment_repository = Singleton(ShipmentRepository)

    shipment_service = Factory(
        ShipmentService,
        repository=shipment_repository,
    )

    user_repository = Singleton(UserRepository)

    user_service = Factory(
        UserService,
        repository=user_repository,
    )
