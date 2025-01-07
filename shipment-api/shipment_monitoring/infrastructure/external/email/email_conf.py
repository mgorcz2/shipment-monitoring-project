"""E-mail config file"""
from fastapi_mail import ConnectionConfig
from dotenv import dotenv_values
from shipment_monitoring.config import config


#config = dotenv_values("shipment_monitoring/.env")
conf = ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_PORT=config.MAIL_PORT,
    MAIL_SERVER=config.MAIL_SERVER,
    MAIL_FROM=config.MAIL_FROM,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,  
)
