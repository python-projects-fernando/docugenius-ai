from typing import Protocol, Optional, List
from backend.core.models.document_field import DocumentField

class DocumentFieldRepository(Protocol):
    async def save(self, document_field: DocumentField) -> DocumentField:
        ...

    async def find_by_id(self, id: int) -> Optional[DocumentField]:
        ...

    async def find_by_name_and_document_type(self, name: str, document_type_id: int) -> Optional[DocumentField]:
        ...

    async def find_all_by_document_type(self, document_type_id: int) -> List[DocumentField]:
        ...

    async def update(self, id: int, document_field: DocumentField) -> Optional[DocumentField]:
        ...

    async def delete(self, id: int) -> bool:
        ...