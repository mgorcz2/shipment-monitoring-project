from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from shipment_monitoring.infrastructure.repositories.shipmentdb import ShipmentRepository
from shipment_monitoring.infrastructure.services.shipment import ShipmentService


class Container(DeclarativeContainer):
    shipment_repository = Singleton(ShipmentRepository)

    shipment_service = Factory(
        ShipmentService,
        repository=shipment_repository,
    )