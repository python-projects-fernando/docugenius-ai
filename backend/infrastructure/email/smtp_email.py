import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.application.email.email import EmailGateway

class SMTPEmailGateway(EmailGateway):
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.email_password = os.getenv("EMAIL_PASSWORD")

        if not all([self.smtp_server, self.email_address, self.email_password]):
            raise ValueError(
                "SMTP_SERVER, EMAIL_ADDRESS, and EMAIL_PASSWORD must be set in environment variables."
            )

    async def send_email(self, to_email: str, subject: str, body: str) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_address, self.email_password)

            text = msg.as_string()
            server.sendmail(self.email_address, to_email, text)
            server.quit()

            print(f"Email sent successfully to {to_email}")
            return True

        except smtplib.SMTPException as e:
            print(f"SMTP error occurred while sending email to {to_email}: {e}")
            return False
        except Exception as e:
            print(f"An error occurred while sending email to {to_email}: {e}")
            return False