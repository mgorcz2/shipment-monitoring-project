from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status

from shipment_monitoring.core.domain.shipment import Shipment, ShipmentIn, ShipmentStatus
from shipment_monitoring.core.domain.location import Location
from shipment_monitoring.infrastructure.dto.shipmentDTO import ShipmentDTO, ShipmentWithDistanceDTO
from shipment_monitoring.infrastructure.services.ishipment import IShipmentService
from shipment_monitoring.infrastructure.services.iuser import IUserService
from shipment_monitoring.container import Container
from shipment_monitoring.core.domain.user import User, UserRole
from shipment_monitoring.core.security import auth
from shipment_monitoring.infrastructure.external.email import email_service
from uuid import UUID
router = APIRouter(
    prefix="/shipments",
    tags=["shipments"],
)

@router.put("/assign", response_model=ShipmentDTO, status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.COURIER)
@inject
async def assign_shipment_to_courier(
    shipment_id: int,
    courier_id: UUID,
    current_user: User = Depends(auth.get_current_user),
    shipment_service: IShipmentService = Depends(Provide[Container.shipment_service]),
    user_service: IUserService = Depends(Provide[Container.user_service])
    ) -> ShipmentDTO | None:
    """The endpoint assigning shipment to courier.

    Args:
        courier_id (int): The id of the courier.
        shipment_id (int): The id of the shipment.
        shipment_service (IShipmentService): The injected service dependency.
        user_service (IUserService): The injected service dependency.
        

    Returns:
        ShipmentDTO | None: The shipment details if updated.
    """
    if await user_service.get_user_by_id(courier_id):
        if shipment := await shipment_service.assign_shipment_to_courier(shipment_id, courier_id):
            return shipment
    raise HTTPException(status_code=404, detail="Shipment not found or wrong courier id")

@router.put("/update_status", response_model=ShipmentDTO, status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.COURIER)
@inject
async def update_status(
    shipment_id: int,
    new_status: ShipmentStatus,
    current_user: User = Depends(auth.get_current_user),
    service: IShipmentService = Depends(Provide[Container.shipment_service])
    ) -> ShipmentDTO | None:
    """The abstract changing shipment status by provided id in the data storage.

    Args:
        courier_id (int): The id of the courier.
        shipment_id (int): The id of the shipment.
        new_status (ShipmentStatus): The new status.

    Returns:
        Any | None: The shipment details if exists.
    """
    if shipment := await service.update_status(current_user.id, shipment_id, new_status):
        return shipment
    raise HTTPException(status_code=404, detail="Shipment not found or not assigned to this courier")


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
        service (IShipmentService): The injected service dependency.

    Returns:
        Any | None: The shipment details if exists.
    """
    if shipment := await service.check_status(shipment_id, recipient_email):
        return shipment
    raise HTTPException(status_code=404, detail="Shipment not found or wrong recipient email")
        


@router.get("/all", response_model=Iterable[ShipmentDTO], status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.COURIER)
@inject
async def get_shipments(
        current_user: User = Depends(auth.get_current_user),
        service: IShipmentService = Depends(Provide[Container.shipment_service])
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

@router.get("/get/{shipment_id}", response_model=ShipmentDTO, status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.COURIER)
@inject
async def get_shipment(
        shipment_id: int,
        current_user: User = Depends(auth.get_current_user),
        service: IShipmentService = Depends(Provide[Container.shipment_service])
    ) -> ShipmentDTO:
    """An endpoint for getting shipment by provided id.

    Args:
        shipment_id (int): The id of the shipment.
        current_user (User): The currently injected authenticated user.
        service (IShipmentService): The injected service dependency.

    Returns:
        ShipmentDTO: The shipment object if exists.
    """
    if shipment := await service.get_shipment_by_id(shipment_id):
        return shipment
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No shipment found with the provided ID.")


@router.delete("/delete/{shipment_id}", status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.COURIER)
@inject
async def delete_shipment(
        shipment_id: int,
        current_user: User = Depends(auth.get_current_user),
        service: IShipmentService = Depends(Provide[Container.shipment_service])
        ) -> dict:
    """The method deleting shipment by provided id.

     Args:
        shipment_id (int): The id of the shipment.
        service (IShipmentService): The injected service dependency.

    Returns:
        Any: The shipment object if deleted.
    """
    if shipment := await service.delete_shipment(shipment_id):
        return dict(shipment)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No shipment found with the provided ID. Try again.")

@router.post("/sort_by/origin", response_model=Iterable[ShipmentWithDistanceDTO],status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.COURIER)
@inject
async def sort_by_origin_distance(
        location: Location,
        current_user: User = Depends(auth.get_current_user),
        service: IShipmentService = Depends(Provide[Container.shipment_service])
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
        shipments = await service.sort_by_distance(current_user.id, location, "origin")
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(error))    
    return shipments


@router.post("/sort_by/destination", response_model=Iterable[ShipmentWithDistanceDTO],status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.COURIER)
@inject
async def sort_by_destination_distance(
        location: Location,
        current_user: User = Depends(auth.get_current_user),
        service: IShipmentService = Depends(Provide[Container.shipment_service])
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
        shipments = await service.sort_by_distance(current_user.id, location, "destination")
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(error))    
    return shipments


@router.post("/add", response_model=ShipmentDTO, status_code=status.HTTP_201_CREATED)
@auth.role_required(UserRole.SENDER)
@inject
async def add_shipment(
        new_shipment: ShipmentIn,
        current_user: User = Depends(auth.get_current_user),
        service: IShipmentService = Depends(Provide[Container.shipment_service])
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
        if new_shipment := await service.add_shipment(new_shipment,sender_id):
            return new_shipment
        #    recipient_email = new_shipment.recipient_email
        #    if recipient_email is not None:
        #        await email_service.send_email(new_shipment.id, "Nadano przesylke do ciebie", recipient_email, "Sprawdz jej status na stronie <url>")
        # The email sending function works, but this section is commented out
        # to protect sensitive configuration data (e.g., email credentials).
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(error))           
                
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(error))    


@router.post("/update", response_model=ShipmentDTO, status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.ADMIN)
@inject
async def update_shipment(
    shipment_id: int,
    data: ShipmentIn,
    current_user: User = Depends(auth.get_current_user),
    service: IShipmentService = Depends(Provide[Container.shipment_service])
    ) -> ShipmentDTO | None:
        """An endpoint for updating shipment data in the reposistory.

        Args:
            shipment_id (int): The id of the shipment.
            data (ShipmentIn): The updated shipment details.
            current_user: User = Depends(auth.get_current_user).
            service (IShipmentService): The injected service dependency.

        Returns:
            ShipmentDTO | None: The updated shipment DTO details if updated.
        """
        try:
            if shipment := await service.update_shipment(shipment_id, data):
                return shipment
            raise HTTPException(status_code=404, detail="Shipment not found or invalid data")
        except ValueError as error:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(error))