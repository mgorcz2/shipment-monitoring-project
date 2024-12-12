from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status

from shipment_monitoring.core.domain.shipment import Shipment, ShipmentIn
from shipment_monitoring.core.domain.location import Location
from shipment_monitoring.infrastructure.dto.shipmentDTO import ShipmentDTO, ShipmentWithDistanceDTO
from shipment_monitoring.infrastructure.services.ishipment import IShipmentService
from shipment_monitoring.container import Container
from shipment_monitoring.core.domain.user import User, UserRole
from shipment_monitoring.core.security import auth
from shipment_monitoring.infrastructure.external.email import email_service

router = APIRouter(
    prefix="/shipments",
    tags=["shipments"],
)

@router.get("/check_status", response_model=ShipmentDTO, status_code=status.HTTP_200_OK)
@inject
async def check_status(
    shipment_id: int,
    recipient_email: str,
    service: IShipmentService = Depends(Provide[Container.shipment_service])
    )-> ShipmentDTO | None:
    """An endpoint getting shipment by provided id and Recipient email.

    Args:
        shipment_id (int): The id of the shipment.
        recipient_email (int): The recipient_email of the shipment.

    Returns:
        Any | None: The shipment details if exists.
    """
    if shipment := await service.check_status(shipment_id, recipient_email):
        return shipment
    raise HTTPException(status_code=404, detail="Shipment not found")
        


@router.get("/all", response_model=Iterable[ShipmentDTO], status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.COURIER)
@inject
async def get_shipments(
        current_user: User = Depends(auth.get_current_user),
        service: IShipmentService = Depends(Provide[Container.shipment_service]),
) -> Iterable[ShipmentDTO]:
    """An endpoint for getting all shipments.

    Args:
        current_user (User): The currently injected authenticated user.
        service (IShipmentService): The injected service dependency.

    Returns:
        Iterable[ShipmentDTO]: Shipments collection.
    """
    shipments = await service.get_all_shipments()
    return shipments

@router.post("/sort_by/origin", response_model=Iterable[ShipmentWithDistanceDTO],status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.COURIER)
@inject
async def sort_by_origin_distance(
        location: Location,
        current_user: User = Depends(auth.get_current_user),
        service: IShipmentService = Depends(Provide[Container.shipment_service]),
) -> Iterable[ShipmentWithDistanceDTO]:
    """An endpoint for sorting shipments by origin distance from courier.

    Args:
        location (Location): Location of courier
        current_user (User): The currently injected authenticated user.
        service (IShipmentService): The injected service dependency.

    Returns:
        Iterable[ShipmentDTO]: Shipments with distance sorted collection.
    """
    try:
        shipments = await service.sort_by_distance(location, "origin")
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(error))    
    return shipments


@router.post("/sort_by/destination", response_model=Iterable[ShipmentWithDistanceDTO],status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.COURIER)
@inject
async def sort_by_destination_distance(
        location: Location,
        current_user: User = Depends(auth.get_current_user),
        service: IShipmentService = Depends(Provide[Container.shipment_service]),
) -> Iterable[ShipmentWithDistanceDTO]:
    """An endpoint for sorting shipments by destination distance from courier.

    Args:
        location (Location): Location of courier
        current_user (User): The currently injected authenticated user.
        service (IShipmentService): The injected service dependency.

    Returns:
        Iterable[ShipmentWithDistanceDTO]: Shipments with distance attribute sorted collection.
    """
    try:
        shipments = await service.sort_by_distance(location, "destination")
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(error))    
    return shipments


@router.post("/add", response_model=ShipmentDTO, status_code=status.HTTP_201_CREATED)
@auth.role_required(UserRole.SENDER)
@inject
async def add_shipment(
        new_shipment: ShipmentIn,
        current_user: User = Depends(auth.get_current_user),
        service: IShipmentService = Depends(Provide[Container.shipment_service]),
) -> ShipmentDTO | None:
    """An endpoint for adding a shipment and sending information to the recipient.

    Args:
        new_shipment (ShipmentIn): The shipment input data.
        current_user (User): The currently injected authenticated user.
        service (IShipmentService): The injected service dependency.

    Returns:
        ShipmentDTO | None The shipment DTO details if exists.
    """
    try:
        sender_id = current_user.id
        new_shipment = await service.add_shipment(new_shipment,sender_id)
        
        #if new_shipment:
        #    recipient_email = new_shipment.recipient_email
        #    if recipient_email is not None:
        #        await email_service.send_email(new_shipment.id, "Nadano przesylke do ciebie", recipient_email, "Sprawdz jej status na stronie <url>")
        # The email sending function works, but this section is commented out
        # to protect sensitive configuration data (e.g., email credentials).
                
                
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(error))    
    return new_shipment or None

