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

router = APIRouter(
    prefix="/shipments",
    tags=["shipments"],
)

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

@router.post("/sort_by_origin", response_model=Iterable[ShipmentWithDistanceDTO],status_code=status.HTTP_200_OK)
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


@router.post("/sort_by_destination", response_model=Iterable[ShipmentWithDistanceDTO],status_code=status.HTTP_200_OK)
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
) -> ShipmentDTO:
    """An endpoint for adding a shipment.

    Args:
        new_shipment (ShipmentIn): The shipment input data.
        current_user (User): The currently injected authenticated user.
        service (IShipmentService): The injected service dependency.

    Returns:
        ShipmentDTO: The shipment DTO details.
    """
    try:
        sender_id = current_user.id
        new_shipment = await service.add_shipment(new_shipment,sender_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(error))    
    return new_shipment

