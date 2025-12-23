from backend.infrastructure.email.smtp_email import SMTPEmailGateway
from backend.application.email.email import EmailGateway

def get_email_gateway() -> EmailGateway:
    return SMTPEmailGateway()