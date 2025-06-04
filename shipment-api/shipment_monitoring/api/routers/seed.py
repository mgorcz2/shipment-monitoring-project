from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from shipment_monitoring.container import Container
from shipment_monitoring.core.domain.user import User, UserRole
from shipment_monitoring.core.security import auth
from shipment_monitoring.infrastructure.services.ishipment import IShipmentService
from shipment_monitoring.infrastructure.services.iuser import IUserService
from shipment_monitoring.seed.seed_data import SHIPMENTS, USERS

router = APIRouter(tags=["seed"])


@router.post("/seed-data", status_code=status.HTTP_201_CREATED)
@auth.role_required(UserRole.ADMIN)
@inject
async def seed_data(
    current_user: User = Depends(auth.get_current_user),
    user_service: IUserService = Depends(Provide[Container.user_service]),
    shipment_service: IShipmentService = Depends(Provide[Container.shipment_service]),
):
    try:
        for user in USERS:
            await user_service.register_user(user)

        sender = await user_service.get_user_by_email("sender")
        courier = await user_service.get_user_by_email("courier")
        for shipment in SHIPMENTS:
            await shipment_service.add_shipment(shipment, sender.id)
        for shipment in await shipment_service.get_all_shipments():
            await shipment_service.assign_shipment_to_courier(shipment.id, courier.id)
        return {"message:": "Data seeded."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
