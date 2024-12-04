from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from shipment_monitoring.core.domain.shipment import Shipment, ShipmentIn
from shipment_monitoring.infrastructure.dto.shipmentDTO import ShipmentDTO
from shipment_monitoring.infrastructure.services.ishipment import IShipmentService
from shipment_monitoring.container import Container
from shipment_monitoring.core.domain.user import User, UserRole
from shipment_monitoring.api.utils.security import auth


router = APIRouter(
    prefix="/shipment",
    tags=["shipment"],
)

@router.get("/all", response_model=Iterable[ShipmentDTO], status_code=200)
@auth.role_required(UserRole.COURIER)
@inject
async def get_shipments(
        current_user: User = Depends(auth.get_current_user),
        service: IShipmentService = Depends(Provide[Container.shipment_service]),
) -> Iterable:
    shipments = await service.get_all_shipments()
    return shipments

@router.post("/add", response_model=Shipment, status_code=201)
@inject
async def add_shipment(
        new_shipment: ShipmentIn,
        service: IShipmentService = Depends(Provide[Container.shipment_service]),
) -> dict:
    new_shipment = await service.add_shipment(new_shipment)
    return new_shipment.model_dump() if new_shipment else {}
