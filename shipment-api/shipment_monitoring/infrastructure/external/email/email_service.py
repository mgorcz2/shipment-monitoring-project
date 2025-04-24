"""Module containing email service implementation."""

from fastapi_mail import FastMail, MessageSchema
from shipment_monitoring.infrastructure.external.email.email_conf import conf

mail = FastMail(conf)


async def send_email(shipment_id: int, subject: str, recipient: str, body: str):
    message = MessageSchema(
        subject=subject, recipients=[recipient], body=body, subtype="html"
    )
    await mail.send_message(message)
