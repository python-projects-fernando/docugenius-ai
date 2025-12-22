from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.application.repositories.generated_document_repository import GeneratedDocumentRepository
from backend.core.models.generated_document import GeneratedDocument as CoreGeneratedDocument
from backend.infrastructure.models.generated_document_model import GeneratedDocumentModel

class MySqlGeneratedDocumentRepository(GeneratedDocumentRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, entity: CoreGeneratedDocument) -> CoreGeneratedDocument:
        db_obj = GeneratedDocumentModel(
            id=entity.id,
            user_id=entity.user_id,
            document_type_id=entity.document_type_id,
            file_path_or_key=entity.file_path_or_key,
            created_at=entity.created_at,
            expires_at=entity.expires_at
        )

        if db_obj.id is None:
            self._session.add(db_obj)
        else:
            existing_db_obj = await self._session.get(GeneratedDocumentModel, db_obj.id)
            if existing_db_obj:
                 existing_db_obj.user_id = db_obj.user_id
                 existing_db_obj.document_type_id = db_obj.document_type_id
                 existing_db_obj.file_path_or_key = db_obj.file_path_or_key
                 existing_db_obj.expires_at = db_obj.expires_at
                 db_obj = existing_db_obj
            else:
                self._session.add(db_obj)

        await self._session.flush()
        await self._session.commit()
        entity.id = db_obj.id
        entity.created_at = db_obj.created_at
        return entity

    async def find_by_id(self, id: int) -> CoreGeneratedDocument | None:
        stmt = select(GeneratedDocumentModel).where(GeneratedDocumentModel.id == id)
        result = await self._session.execute(stmt)
        db_obj = result.scalar_one_or_none()

        if not db_obj:
            return None

        return CoreGeneratedDocument(
            id=db_obj.id,
            user_id=db_obj.user_id,
            document_type_id=db_obj.document_type_id,
            file_path_or_key=db_obj.file_path_or_key,
            created_at=db_obj.created_at,
            expires_at=db_obj.expires_at
        )

    async def find_by_user_id(self, user_id: int) -> List[CoreGeneratedDocument]:
        stmt = select(GeneratedDocumentModel).where(GeneratedDocumentModel.user_id == user_id)
        result = await self._session.execute(stmt)
        db_objs = result.scalars().all()

        return [
            CoreGeneratedDocument(
                id=db_obj.id,
                user_id=db_obj.user_id,
                document_type_id=db_obj.document_type_id,
                file_path_or_key=db_obj.file_path_or_key,
                created_at=db_obj.created_at,
                expires_at=db_obj.expires_at
            )
            for db_obj in db_objs
        ]