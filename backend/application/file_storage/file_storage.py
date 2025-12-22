from typing import Protocol

class FileStorageGateway(Protocol):
    async def save_document(self, content: bytes, filename: str) -> str:
        ...

    async def get_file_url(self, location_identifier: str) -> str:
        ...