"""E-mail config file"""
from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="mail_username",
    MAIL_PASSWORD="mail_password",
    MAIL_FROM="mail_from@example.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,  
)