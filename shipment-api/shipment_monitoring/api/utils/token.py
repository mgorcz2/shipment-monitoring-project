from pydantic import BaseModel, ConfigDict
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
from shipment_monitoring.api.utils import consts

class TokenDTO(BaseModel):
    access_token: str
    token_type: str
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        #.now(datetime.timezone.utc)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, consts.SECRET_KEY, algorithm=consts.ALGORITHM)
    return encoded_jwt
