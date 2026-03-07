from typing import Optional, List
import logging # Importe logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update, func, asc, exists
from backend.application.repositories.document_type_repository import DocumentTypeRepository
from backend.core.models.document_type import DocumentType as CoreDocumentType
from backend.infrastructure.models.document_type_model import DocumentTypeModel as InfraDocumentType
from backend.infrastructure.models.document_field_model import DocumentFieldModel as InfraDocumentField

# Configure um logger básico (você pode usar um logger mais sofisticado se preferir)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    async def find_all_paginated(self, offset: int, limit: int) -> List[CoreDocumentType]:
        result = await self._db_session.execute(
                select(InfraDocumentType).order_by(InfraDocumentType.name.asc()).offset(offset).limit(limit)
            )
        infra_doc_types = result.scalars().all()
        return [
                CoreDocumentType(
                    id=dt.id,
                    name=dt.name,
                    description=dt.description
                ) for dt in infra_doc_types
            ]

    async def count_all(self) -> int:
        result = await self._db_session.execute(select(func.count(InfraDocumentType.id)))
        return result.scalar()

    async def find_with_fields(self) -> List[CoreDocumentType]:
        logger.info("DEBUG: find_with_fields called") # Log
        # Usando uma subquery explícita correlacionada
        # Criamos uma query para document_fields filtrando por um ID hipotético (será substituído pela correlação)
        # Correlacionamos com a query externa usando dt.id
        subq = select(1).select_from(InfraDocumentField).where(
            InfraDocumentField.document_type_id == InfraDocumentType.id).exists()
        # Usando .exists() no SQLAlchemy para gerar o EXISTS correto

        query = select(InfraDocumentType).where(subq)
        logger.info(f"DEBUG: Executing query: {query}") # Log da query (pode ser verboso)
        result = await self._db_session.execute(query)
        infra_doc_types = result.scalars().all()
        logger.info(f"DEBUG: find_with_fields returned {len(infra_doc_types)} items") # Log
        return [
            CoreDocumentType(
                id=dt.id,
                name=dt.name,
                description=dt.description
            ) for dt in infra_doc_types
        ]

    async def find_with_fields_paginated(self, offset: int, limit: int) -> List[CoreDocumentType]:
        logger.info(f"DEBUG: find_with_fields_paginated called with offset={offset}, limit={limit}") # Log
        # Usando a mesma lógica corrigida
        subq = select(1).select_from(InfraDocumentField).where(
            InfraDocumentField.document_type_id == InfraDocumentType.id).exists()

        query = select(InfraDocumentType).where(subq).order_by(InfraDocumentType.name.asc()).offset(offset).limit(limit)
        logger.info(f"DEBUG: Executing query: {query}") # Log da query (pode ser verboso)
        result = await self._db_session.execute(query)
        infra_doc_types = result.scalars().all()
        logger.info(f"DEBUG: find_with_fields_paginated returned {len(infra_doc_types)} items") # Log
        return [
            CoreDocumentType(
                id=dt.id,
                name=dt.name,
                description=dt.description
            ) for dt in infra_doc_types
        ]

    async def count_with_fields(self) -> int:
        logger.info("DEBUG: count_with_fields called") # Log
        # Usando a mesma lógica corrigida
        subq = select(1).select_from(InfraDocumentField).where(
            InfraDocumentField.document_type_id == InfraDocumentType.id).exists()

        query = select(func.count(InfraDocumentType.id)).where(subq)
        logger.info(f"DEBUG: Executing query: {query}") # Log da query (pode ser verboso)
        result = await self._db_session.execute(query)
        count_result = result.scalar() or 0
        logger.info(f"DEBUG: count_with_fields returned {count_result}") # Log
        return count_result