from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from shipment_monitoring.core.domain.shipment import Shipment
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
