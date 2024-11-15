from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from shipment_monitoring.core.domain.shipment import Shipment, ShipmentIn
from shipment_monitoring.infrastructure.services.ishipment import IShipmentService
from shipment_monitoring.container import Container

router = APIRouter()

@router.get("/all", response_model=Iterable[Shipment], status_code=200)
@inject
async def get_shipments(
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
