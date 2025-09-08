"""Module containing authentication and authorization methods."""

from functools import wraps

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from shipment_monitoring.config import config
from shipment_monitoring.container import Container
from shipment_monitoring.core.domain.user import User, UserRole
from shipment_monitoring.core.security import consts
from shipment_monitoring.infrastructure.dto.userDTO import UserDTO
from shipment_monitoring.infrastructure.services.iuser import IUserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


@inject
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: IUserService = Depends(Provide[Container.user_service]),
) -> UserDTO:
    """The method authenticating the user based on a JWT token.

    Args:
        token (str): JWT bearer token provided by the oauth2_scheme dependency.
        service (IUserService):The injected service dependency.

    Raises:
        HTTPException: With status code 401 (Unauthorized)

    Returns:
        User: The user object if authenticated.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[consts.ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await service.get_user_by_id(id)
    if user is None:
        raise credentials_exception
    return user


def role_required(required_role: list[UserRole]):
    """A decorator that enforces role-based access control for endpoint methods.

    Args:
        required_role (list): The roles required to access the decorated endpoint.
    """

    def decorator(func):
        @wraps(func)  # wraps some function
        async def wrapper(
            *args, current_user: User = Depends(get_current_user), **kwargs
        ):
            if (
                current_user.role not in required_role
                and current_user.role != UserRole.ADMIN
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No permission to access this resource.",
                )
            return await func(*args, current_user=current_user, **kwargs)

        return wrapper

    return decorator
