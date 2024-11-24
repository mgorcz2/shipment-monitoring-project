from pydantic import BaseModel, ConfigDict


class UserIn(BaseModel): #klasa ktora pomaga stworzyc obiekt w bazie danych (id samo sie incrementuje bo to klucz glowny)
    username: str
    password: str


class User(UserIn):
    id: int

    model_config = ConfigDict(from_attributes=True, extra='ignore')
