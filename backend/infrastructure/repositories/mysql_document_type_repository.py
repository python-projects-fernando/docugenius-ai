from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from backend.application.repositories.document_type_repository import DocumentTypeRepository
from backend.core.models.document_type import DocumentType as CoreDocumentType
from backend.infrastructure.models.document_type_model import DocumentTypeModel as InfraDocumentType

class MySqlDocumentTypeRepository(DocumentTypeRepository):

    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def save(self, document_type: CoreDocumentType) -> CoreDocumentType:
        infra_doc_type = InfraDocumentType(
            id=document_type.id,
            name=document_type.name,
            description=document_type.description
        )

        self._db_session.add(infra_doc_type)
        await self._db_session.commit()
        await self._db_session.refresh(infra_doc_type)

        saved_core_entity = CoreDocumentType(
            id=infra_doc_type.id,
            name=infra_doc_type.name,
            description=infra_doc_type.description
        )
        return saved_core_entity

    async def find_by_id(self, id: int) -> Optional[CoreDocumentType]:
        result = await self._db_session.execute(
            select(InfraDocumentType).where(InfraDocumentType.id == id)
        )
        infra_doc_type = result.scalars().first()
        if infra_doc_type:
            return CoreDocumentType(
                id=infra_doc_type.id,
                name=infra_doc_type.name,
                description=infra_doc_type.description
            )
        return None

    async def find_by_name(self, name: str) -> Optional[CoreDocumentType]:
        result = await self._db_session.execute(
            select(InfraDocumentType).where(InfraDocumentType.name == name)
        )
        infra_doc_type = result.scalars().first()
        if infra_doc_type:
            return CoreDocumentType(
                id=infra_doc_type.id,
                name=infra_doc_type.name,
                description=infra_doc_type.description
            )
        return None

    async def find_all(self) -> List[CoreDocumentType]:
        result = await self._db_session.execute(select(InfraDocumentType))
        infra_doc_types = result.scalars().all()
        return [
            CoreDocumentType(
                id=dt.id,
                name=dt.name,
                description=dt.description
            ) for dt in infra_doc_types
        ]

    async def update(self, id: int, document_type: CoreDocumentType) -> Optional[CoreDocumentType]:
        stmt = (
            update(InfraDocumentType).
            where(InfraDocumentType.id == id).
            values(
                name=document_type.name,
                description=document_type.description
            )
        )
        result = await self._db_session.execute(stmt)

        if result.rowcount == 0:
            await self._db_session.commit()
            return None

        await self._db_session.commit()
        return await self.find_by_id(id)

    async def delete(self, id: int) -> bool:
        stmt = delete(InfraDocumentType).where(InfraDocumentType.id == id)
        result = await self._db_session.execute(stmt)
        success = result.rowcount > 0
        await self._db_session.commit()
        return success
