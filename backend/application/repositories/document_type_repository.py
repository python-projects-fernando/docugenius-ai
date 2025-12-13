from typing import Protocol, Optional, List
from backend.core.models.document_type import DocumentType

class DocumentTypeRepository(Protocol):
    async def save(self, document_type: DocumentType) -> DocumentType:
        ...

    async def find_by_id(self, id: int) -> Optional[DocumentType]:
        ...

    async def find_by_name(self, name: str) -> Optional[DocumentType]:
        ...

    async def find_all(self) -> List[DocumentType]:
        ...

    async def update(self, id: int, document_type: DocumentType) -> Optional[DocumentType]:
        ...

    async def delete(self, id: int) -> bool:
        ...
