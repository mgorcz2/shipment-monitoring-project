from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from shipment_monitoring.infrastructure.repositories.shipmentdb import ShipmentRepository
from shipment_monitoring.infrastructure.repositories.userdb import UserRepository
from shipment_monitoring.infrastructure.services.shipment import ShipmentService
from shipment_monitoring.infrastructure.services.user import UserService


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