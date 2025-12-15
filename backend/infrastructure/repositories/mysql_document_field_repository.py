from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update, func
from backend.application.repositories.document_field_repository import DocumentFieldRepository
from backend.core.models.document_field import DocumentField as CoreDocumentField
from backend.infrastructure.models.document_field_model import DocumentFieldModel

class MySqlDocumentFieldRepository(DocumentFieldRepository):
    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def save(self, document_field: CoreDocumentField) -> CoreDocumentField:
        infra_doc_field = DocumentFieldModel(
            id=document_field.id,
            document_type_id=document_field.document_type_id,
            name=document_field.name,
            field_type=document_field.field_type,
            is_required=document_field.is_required,
            description=document_field.description
        )

        if document_field.id is not None:
            self._db_session.add(infra_doc_field)
            await self._db_session.commit()
            await self._db_session.refresh(infra_doc_field)
        else:
            self._db_session.add(infra_doc_field)
            await self._db_session.commit()
            await self._db_session.refresh(infra_doc_field)

        saved_core_entity = CoreDocumentField(
            id=infra_doc_field.id,
            document_type_id=infra_doc_field.document_type_id,
            name=infra_doc_field.name,
            field_type=infra_doc_field.field_type,
            is_required=infra_doc_field.is_required,
            description=infra_doc_field.description
        )
        return saved_core_entity

    async def find_by_id(self, id: int) -> Optional[CoreDocumentField]:
        result = await self._db_session.execute(
            select(DocumentFieldModel).where(DocumentFieldModel.id == id)
        )
        infra_doc_field = result.scalars().first()
        if infra_doc_field:
            return CoreDocumentField(
                id=infra_doc_field.id,
                document_type_id=infra_doc_field.document_type_id,
                name=infra_doc_field.name,
                field_type=infra_doc_field.field_type,
                is_required=infra_doc_field.is_required,
                description=infra_doc_field.description
            )
        return None

    async def find_by_name_and_document_type(self, name: str, document_type_id: int) -> Optional[CoreDocumentField]:
        result = await self._db_session.execute(
            select(DocumentFieldModel)
            .where(DocumentFieldModel.name == name)
            .where(DocumentFieldModel.document_type_id == document_type_id)
        )
        infra_doc_field = result.scalars().first()
        if infra_doc_field:
            return CoreDocumentField(
                id=infra_doc_field.id,
                document_type_id=infra_doc_field.document_type_id,
                name=infra_doc_field.name,
                field_type=infra_doc_field.field_type,
                is_required=infra_doc_field.is_required,
                description=infra_doc_field.description
            )
        return None

    async def find_all_by_document_type(self, document_type_id: int) -> List[CoreDocumentField]:
        result = await self._db_session.execute(
            select(DocumentFieldModel)
            .where(DocumentFieldModel.document_type_id == document_type_id)
        )
        infra_doc_fields = result.scalars().all()
        return [
            CoreDocumentField(
                id=field.id,
                document_type_id=field.document_type_id,
                name=field.name,
                field_type=field.field_type,
                is_required=field.is_required,
                description=field.description
            ) for field in infra_doc_fields
        ]

    async def update(self, id: int, document_field: CoreDocumentField) -> Optional[CoreDocumentField]:
        stmt = (
            update(DocumentFieldModel).
            where(DocumentFieldModel.id == id).
            values(
                name=document_field.name,
                field_type=document_field.field_type,
                is_required=document_field.is_required,
                description=document_field.description
            )
        )
        result = await self._db_session.execute(stmt)

        if result.rowcount == 0:
            await self._db_session.commit()
            return None

        await self._db_session.commit()
        return await self.find_by_id(id)

    async def delete(self, id: int) -> bool:
        stmt = delete(DocumentFieldModel).where(DocumentFieldModel.id == id)
        result = await self._db_session.execute(stmt)
        success = result.rowcount > 0
        await self._db_session.commit()
        return success