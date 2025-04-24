"""A module providing configuration variables."""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """A class containing base settings configuration."""

    model_config = SettingsConfigDict(extra="ignore")


class AppConfig(BaseConfig):
    """A class containing app's configuration."""

    DB_HOST: Optional[str] = None
    DB_NAME: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None

    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[str] = None
    MAIL_PORT: Optional[str] = None
    MAIL_SERVER: Optional[str] = None

    SECRET_KEY: Optional[str] = None


config = AppConfig()
