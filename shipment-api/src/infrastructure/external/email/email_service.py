import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from src.config import config


class EmailService:
    """Serwis do wysyłania emaili przez SMTP"""

    def __init__(self):
        self.smtp_server = config.MAIL_SERVER
        self.smtp_port = config.MAIL_PORT
        self.from_email = config.MAIL_FROM

    async def send_email(
        self, to_email: str, subject: str, body: str, is_html: bool = False
    ) -> bool:
        try:
            msg = MIMEMultipart()
            msg["From"] = self.from_email
            msg["To"] = to_email
            msg["Subject"] = subject

            mime_type = "html" if is_html else "plain"
            msg.attach(MIMEText(body, mime_type))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                text = msg.as_string()
                server.sendmail(self.from_email, to_email, text)

            return True

        except Exception as e:
            print(f"Błąd wysyłania emaila: {e}")
            return False

    async def send_welcome_email(
        self, user_email: str, first_name: str, address: str
    ) -> bool:
        """Wysyła email powitalny dla nowego klienta"""
        subject = "Witamy w paczkuj.to!"

        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #01c363;">Witaj {first_name}!</h2>
                
                <p>Twoje konto klienta zostało pomyślnie utworzone w <strong>paczkuj.to</strong>.</p>
                
                <div style="background: #f7f7f7; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #01c363;">Twoje dane:</h3>
                    <p><strong>Email:</strong> {user_email}</p>
                    <p><strong>Imię:</strong> {first_name}</p>
                    <p><strong>Adres:</strong> {address}</p>
                </div>
                
                <p>Możesz teraz korzystać z wszystkich funkcji naszej platformy:</p>
                <ul style="color: #555;">
                    <li>Śledzenie przesyłek w czasie rzeczywistym</li>
                    <li>Historia wszystkich zamówień</li>
                    <li>Zarządzanie danymi profilu</li>
                    <li>Powiadomienia o statusie przesyłek</li>
                </ul>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:3000/login" 
                       style="background: #01c363; color: white; padding: 12px 24px; 
                              text-decoration: none; border-radius: 6px; font-weight: bold;">
                        Zaloguj się do paczkuj.to
                    </a>
                </div>
                
                <hr style="border: 1px solid #eee; margin: 30px 0;">
                
                <p style="color: #888; font-size: 14px;">
                    Pozdrowienia,<br>
                    <strong style="color: #01c363;">Zespół paczkuj.to</strong>
                </p>
            </div>
        </body>
        </html>
        """

        return await self.send_email(user_email, subject, body, is_html=True)

    async def send_shipment_notification(
        self, recipient_email: str, shipment_id: int, status: str
    ) -> bool:
        """Wysyła powiadomienie do odbiorcy o zmianie statusu przesyłki"""
        subject = f"Aktualizacja przesyłki #{shipment_id}"

        status_display = {
            "created": "Utworzona",
            "picked_up": "Odebrana",
            "in_transit": "W transporcie",
            "delivered": "Dostarczona",
            "cancelled": "Anulowana",
        }
        status_name = status_display.get(status, status)

        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #01c363;">Aktualizacja przesyłki</h2>
                
                <p>Twoja przesyłka o numerze <strong>#{shipment_id}</strong> zmieniła status.</p>
                
                <div style="background: #f7f7f7; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #01c363;">Aktualny status:</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #01c363; margin: 5px 0;">{status_name}</p>
                </div>
                
                <p>Aby sprawdzić szczegóły przesyłki, kliknij poniższy przycisk:</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:3000/track/{shipment_id}?email={recipient_email}" 
                       style="background: #01c363; color: white; padding: 12px 24px; 
                              text-decoration: none; border-radius: 6px; font-weight: bold;">
                        Śledź przesyłkę
                    </a>
                </div>
                
                <p>Dziękujemy za skorzystanie z naszych usług!</p>
                
                <hr style="border: 1px solid #eee; margin: 30px 0;">
                
                <p style="color: #888; font-size: 14px;">
                    Jeśli masz pytania, skontaktuj się z naszym działem obsługi klienta.<br>
                    <strong style="color: #01c363;">Zespół paczkuj.to</strong>
                </p>
            </div>
        </body>
        </html>
        """

        return await self.send_email(recipient_email, subject, body, is_html=True)

    async def send_package_created_email(
        self, recipient_email: str, shipment_id: int
    ) -> bool:
        """Wysyła powiadomienie do odbiorcy o nadaniu paczki"""
        subject = "Powiadomienie: Nadano Twoją przesyłkę"

        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #01c363;">Twoja przesyłka została nadana!</h2>
                
                <p>Przesyłka o numerze <strong>#{shipment_id}</strong> została nadana i jest w drodze do Ciebie.</p>
                
                <div style="background: #f7f7f7; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #01c363;">Numer przesyłki:</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #01c363;">#{shipment_id}</p>
                </div>
                
                <p>Aby sprawdzić aktualny status przesyłki, kliknij poniższy przycisk:</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:3000/track/{shipment_id}?email={recipient_email}" 
                       style="background: #01c363; color: white; padding: 12px 24px; 
                              text-decoration: none; border-radius: 6px; font-weight: bold;">
                        Śledź przesyłkę
                    </a>
                </div>
                
                <p>Dziękujemy za skorzystanie z naszych usług!</p>
                
                <hr style="border: 1px solid #eee; margin: 30px 0;">
                
                <p style="color: #888; font-size: 14px;">
                    Jeśli masz pytania, skontaktuj się z naszym działem obsługi klienta.<br>
                    <strong style="color: #01c363;">Zespół paczkuj.to</strong>
                </p>
            </div>
        </body>
        </html>
        """

        return await self.send_email(recipient_email, subject, body, is_html=True)
