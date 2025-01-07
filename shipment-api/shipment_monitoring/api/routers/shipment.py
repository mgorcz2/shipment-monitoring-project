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
    ) -> ShipmentDTO:
    """The endpoint assigning shipment to courier.

    Args:
        courier_id (int): The id of the courier.
        shipment_id (int): The id of the shipment.
        shipment_service (IShipmentService): The injected service dependency.
        user_service (IUserService): The injected service dependency.
        

    Returns:
        ShipmentDTO: The shipment details if updated.
    """
    if await user_service.get_user_by_id(courier_id):
        if shipment := await shipment_service.assign_shipment_to_courier(shipment_id, courier_id):
            return shipment
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found or wrong courier id")


@router.put("/update_status", response_model=ShipmentDTO, status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.COURIER)
@inject
async def update_status(
    shipment_id: int,
    new_status: ShipmentStatus,
    current_user: User = Depends(auth.get_current_user),
    service: IShipmentService = Depends(Provide[Container.shipment_service])
    ) -> ShipmentDTO:
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
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found or not assigned to this courier")


@router.get("/check_status", response_model=ShipmentDTO, status_code=status.HTTP_200_OK)
@inject
async def check_status(
    shipment_id: int,
    recipient_email: str,
    service: IShipmentService = Depends(Provide[Container.shipment_service])
    )-> ShipmentDTO:
    """An endpoint getting shipment by provided id and Recipient email.

    Args:
        shipment_id (int): The id of the shipment.
        recipient_email (int): The recipient_email of the shipment.
        service (IShipmentService): The injected service dependency.

    Returns:
       ShipmentDTO: The shipment details if exists.
    """
    if shipment := await service.check_status(shipment_id, recipient_email):
        return shipment
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found or wrong recipient email")
        

@router.get("/all", response_model=Iterable[ShipmentDTO], status_code=status.HTTP_200_OK)
@inject
async def get_all_shipments(
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
    if shipments := await service.get_all_shipments():
        if current_user.role == "admin":
            return shipments
        if current_user.role == "courier":
            return [shipment for shipment in shipments if shipment.courier_id==current_user.id]
        if current_user.role == "sender":
            return [shipment for shipment in shipments if shipment.sender_id==current_user.id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No shipments found.")


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
        dict: The shipment object if deleted.
    """
    if shipment := await service.delete_shipment(shipment_id):
        return dict(shipment)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No shipment found with the provided ID. Try again.")


@router.post("/sort_by/distance",status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.COURIER)
@inject
async def sort_by_distance(
        location: Location,
        current_user: User = Depends(auth.get_current_user),
        service: IShipmentService = Depends(Provide[Container.shipment_service])
    ) -> Iterable[ShipmentWithDistanceDTO] | None:
    """An endpoint for sorting shipments by origin distance from courier.

    Args:
        location (Location): Location of courier
        current_user (User): The currently injected authenticated user.
        service (IShipmentService): The injected service dependency.

    Returns:
        Iterable[ShipmentDTO]: Shipments with distance sorted collection.
    """
    try:
        shipments = await service.sort_by_distance(current_user.id, location)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(error))    
    if shipments:
        return shipments
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No shipments found with this courier.")


@router.post("/add", response_model=ShipmentDTO, status_code=status.HTTP_201_CREATED)
@auth.role_required(UserRole.SENDER)
@inject
async def add_shipment(
        new_shipment: ShipmentIn,
        current_user: User = Depends(auth.get_current_user),
        service: IShipmentService = Depends(Provide[Container.shipment_service])
    ) -> ShipmentDTO:
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
            recipient_email = new_shipment.recipient_email
            if recipient_email is not None:
                await email_service.send_email(
                    new_shipment.id, 
                    subject="Powiadomienie: Nadano Twoją przesyłkę", 
                    recipient=recipient_email, 
                    body=f"""
                        <h2>Twoja przesyłka została nadana!</h2>
                        <p>Przesyłka o numerze <strong>{new_shipment.id}</strong> została nadana i jest w drodze do Ciebie.</p>
                        <p>Aby sprawdzić jej aktualny status, odwiedź poniższy link:</p>
                        <p><a href="http://localhost:8000/shipments/check_status?shipment_id={new_shipment.id}&recipient_email={recipient_email}" target="_blank">Śledź przesyłkę</a></p>
                        <p>Dziękujemy za skorzystanie z naszych usług!</p>
                        <hr>
                        <p>Jeśli masz pytania, skontaktuj się z naszym działem obsługi klienta.</p>
                        """
                    )
        return new_shipment
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(error))    


@router.put("/update/{shipment_id}", response_model=ShipmentDTO, status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.ADMIN)
@inject
async def update_shipment(
    shipment_id: int,
    data: ShipmentIn,
    current_user: User = Depends(auth.get_current_user),
    service: IShipmentService = Depends(Provide[Container.shipment_service])
    ) -> ShipmentDTO:
        """An endpoint for updating shipment data in the reposistory.

        Args:
            shipment_id (int): The id of the shipment.
            data (ShipmentIn): The updated shipment details.
            current_user: User = Depends(auth.get_current_user).
            service (IShipmentService): The injected service dependency.

        Returns:
            ShipmentDTO: The updated shipment DTO details if updated.
        """
        try:
            if shipment := await service.update_shipment(shipment_id, data):
                return shipment
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found or invalid data")
        except ValueError as error:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(error))
