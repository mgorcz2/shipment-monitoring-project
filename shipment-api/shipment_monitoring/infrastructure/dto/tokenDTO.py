"""A module containing DTO models for output tokens."""

from pydantic import BaseModel, ConfigDict
class TokenDTO(BaseModel):
    """A model representing DTO for token data."""
    access_token: str
    token_type: str
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )
    