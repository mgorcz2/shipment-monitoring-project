from pydantic import BaseModel, ConfigDict
class TokenDTO(BaseModel):
    access_token: str
    token_type: str
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )