from pydantic import BaseModel, ConfigDict


class UserIn(BaseModel):
    login: str
    password: str


class User(UserIn):
    id: int

    model_config = ConfigDict(from_attributes=True, extra='ignore')
