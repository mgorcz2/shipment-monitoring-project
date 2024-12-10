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
    shipments = await service.get_all_shipments()
    return shipments

@router.post("/sort_by_origin", response_model=Iterable[ShipmentWithDistanceDTO],status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.COURIER)
@inject
async def sort_by_origin_distance(
        location: Location,
        current_user: User = Depends(auth.get_current_user),
        service: IShipmentService = Depends(Provide[Container.shipment_service]),
) -> Iterable[ShipmentDTO]:
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
) -> Iterable:
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
) -> dict:
    try:
        sender_id = current_user.id
        new_shipment = await service.add_shipment(new_shipment,sender_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(error))    
    return new_shipment.model_dump() if new_shipment else {}

