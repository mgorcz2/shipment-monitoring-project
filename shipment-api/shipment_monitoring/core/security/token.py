"""A module containing JWT token creation."""

from datetime import datetime, timedelta, timezone

from jose import jwt
from shipment_monitoring.config import config
from shipment_monitoring.core.security import consts


def create_access_token(data: dict):
    """Generate a JSON Web Token(JWT).

    Args:
        data (dict): A dictionary containing the claims to be encoded in the token.
        expires_delta (Optional[timedelta], optional):  Custom expiration time for the token.

    Returns:
        _type_: A JWT-encoded access token as a string.
    """
    if not data.get("sub"):
        raise ValueError("Token payload must contain a non-empty 'sub'")

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=consts.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=consts.ALGORITHM)
    return encoded_jwt
