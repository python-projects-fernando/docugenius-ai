from typing import Protocol

class EmailGateway(Protocol):
    async def send_email(self, to_email: str, subject: str, body: str) -> bool:
        ...