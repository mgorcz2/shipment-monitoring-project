from shipment_monitoring.container import Container
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from shipment_monitoring.infrastructure.services.iuser import IUserService
from dependency_injector.wiring import Provide, inject
from shipment_monitoring.api.utils import consts

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  #ktory endpoint przekazuje tokeny

@inject
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: IUserService = Depends(Provide[Container.user_service])
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, consts.SECRET_KEY, algorithms=[consts.ALGORITHM]
        )
        id: str = payload.get("sub")
        if id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await service.get_user_by_id(id)
    if user is None:
        raise credentials_exception
    return user
