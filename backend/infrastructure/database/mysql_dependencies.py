from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.infrastructure.database.mysql_config import async_sessionmaker_instance
from backend.infrastructure.repositories.mysql_document_type_repository import MySqlDocumentTypeRepository
from backend.infrastructure.repositories.mysql_user_repository import MySqlUserRepository


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker_instance() as session:
        yield session

def get_mysql_document_type_repository(session: AsyncSession = Depends(get_db_session)):
    return MySqlDocumentTypeRepository(session)


def get_mysql_user_repository(session: AsyncSession = Depends(get_db_session)):
    return MySqlUserRepository(session)