from shipment_monitoring.container import Container
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from shipment_monitoring.infrastructure.services.iuser import IUserService
from dependency_injector.wiring import Provide, inject

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password) -> str:
    return pwd_context.hash(password)

def verify_password(user_password, crypt_password):
    if pwd_context.verify(user_password, crypt_password):
        return True
    return False

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  #ktory endpoint przekazuje tokeny

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        #.now(datetime.timezone.utc)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await service.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user
