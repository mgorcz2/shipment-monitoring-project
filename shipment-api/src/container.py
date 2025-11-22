from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from src.infrastructure.external.email.email_service import EmailService
from src.infrastructure.repositories.clientdb import ClientRepository
from src.infrastructure.repositories.packagedb import PackageRepository
from src.infrastructure.repositories.shipmentdb import ShipmentRepository
from src.infrastructure.repositories.staffdb import StaffRepository
from src.infrastructure.repositories.userdb import UserRepository
from src.infrastructure.services.client import ClientService
from src.infrastructure.services.package import PackageService
from src.infrastructure.services.shipment import ShipmentService
from src.infrastructure.services.staff import StaffService
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

    staff_repository = Singleton(StaffRepository)

    staff_service = Factory(
        StaffService, staff_repository=staff_repository, user_service=user_service
    )
    email_service = Singleton(EmailService)
    client_repository = Singleton(ClientRepository)

    client_service = Factory(
        ClientService,
        repository=client_repository,
        user_service=user_service,
        email_service=email_service,
    )

    package_repository = Singleton(PackageRepository)

    package_service = Factory(
        PackageService, repository=package_repository, shipment_service=shipment_service
    )
