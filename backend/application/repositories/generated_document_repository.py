from typing import Protocol
from typing import List
from backend.core.models.generated_document import GeneratedDocument

class GeneratedDocumentRepository(Protocol):
    async def save(self, entity: GeneratedDocument) -> GeneratedDocument:
        ...

    async def find_by_id(self, id: int) -> GeneratedDocument | None:
        ...

    async def find_by_user_id(self, user_id: int) -> List[GeneratedDocument]:
        ...