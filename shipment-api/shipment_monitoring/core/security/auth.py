from shipment_monitoring.container import Container
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from shipment_monitoring.infrastructure.services.iuser import IUserService
from dependency_injector.wiring import Provide, inject
from shipment_monitoring.core.security import consts
from shipment_monitoring.core.domain.user import User
from functools import wraps
from shipment_monitoring.core.shared.UserRoleEnum import UserRole
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  #ktory endpoint przekazuje tokeny

@inject
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: IUserService = Depends(Provide[Container.user_service])
    ):
    '''Validates the JWT token and retrieves the authenticated user.'''
    
    
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

from functools import wraps
from fastapi import Depends, HTTPException, status



def role_required(required_role: str):
    
    '''Decorator for verifying user roles before accessing an endpoint.'''
    
    def decorator(func):
        @wraps(func)  #wraps some function
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if current_user.role != required_role and current_user.role != UserRole.ADMIN:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No permission to access this resource.",
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator
