from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update, func
from backend.application.repositories.user_repository import UserRepository
from backend.core.models.user import User as CoreUser
from backend.infrastructure.models.user_model import UserModel
from backend.core.value_objects.hashed_password import HashedPassword

class MySqlUserRepository(UserRepository):
    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def save(self, user: CoreUser) -> CoreUser:
        infra_user = UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.hashed_password.value,
            role=user.role,
            is_active=user.is_active,
        )

        if user.id is not None:
            self._db_session.add(infra_user)
            await self._db_session.commit()
            await self._db_session.refresh(infra_user)
        else:
            self._db_session.add(infra_user)
            await self._db_session.commit()
            await self._db_session.refresh(infra_user)

        saved_core_entity = CoreUser(
            id=infra_user.id,
            username=infra_user.username,
            email=infra_user.email,
            hashed_password=HashedPassword(value=infra_user.password_hash),
            role=infra_user.role,
            is_active=infra_user.is_active,
            created_at=infra_user.created_at,
            updated_at=infra_user.updated_at
        )
        return saved_core_entity

    async def find_by_id(self, id: int) -> Optional[CoreUser]:
        result = await self._db_session.execute(
            select(UserModel).where(UserModel.id == id)
        )
        infra_user = result.scalars().first()
        if infra_user:
            return CoreUser(
                id=infra_user.id,
                username=infra_user.username,
                email=infra_user.email,
                hashed_password=HashedPassword(value=infra_user.password_hash),
                role=infra_user.role,
                is_active=infra_user.is_active,
                created_at=infra_user.created_at,
                updated_at=infra_user.updated_at
            )
        return None

    async def find_by_username(self, username: str) -> Optional[CoreUser]:
        result = await self._db_session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        infra_user = result.scalars().first()
        if infra_user:
            return CoreUser(
                id=infra_user.id,
                username=infra_user.username,
                email=infra_user.email,
                hashed_password=HashedPassword(value=infra_user.password_hash),
                role=infra_user.role,
                is_active=infra_user.is_active,
                created_at=infra_user.created_at,
                updated_at=infra_user.updated_at
            )
        return None

    async def find_by_email(self, email: str) -> Optional[CoreUser]:
        result = await self._db_session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        infra_user = result.scalars().first()
        if infra_user:
            return CoreUser(
                id=infra_user.id,
                username=infra_user.username,
                email=infra_user.email,
                hashed_password=HashedPassword(value=infra_user.password_hash),
                role=infra_user.role,
                is_active=infra_user.is_active,
                created_at=infra_user.created_at,
                updated_at=infra_user.updated_at
            )
        return None

    async def find_all(self) -> List[CoreUser]:
        result = await self._db_session.execute(select(UserModel))
        infra_users = result.scalars().all()
        return [
            CoreUser(
                id=usr.id,
                username=usr.username,
                email=usr.email,
                hashed_password=HashedPassword(value=usr.password_hash),
                role=usr.role,
                is_active=usr.is_active,
                created_at=usr.created_at,
                updated_at=usr.updated_at
            ) for usr in infra_users
        ]

    async def find_all_paginated(self, offset: int, limit: int) -> List[CoreUser]:
        result = await self._db_session.execute(
            select(UserModel).offset(offset).limit(limit)
        )
        infra_users = result.scalars().all()
        return [
            CoreUser(
                id=usr.id,
                username=usr.username,
                email=usr.email,
                hashed_password=HashedPassword(value=usr.password_hash),
                role=usr.role,
                is_active=usr.is_active,
                created_at=usr.created_at,
                updated_at=usr.updated_at
            ) for usr in infra_users
        ]

    async def count_all(self) -> int:
        result = await self._db_session.execute(select(func.count(UserModel.id)))
        return result.scalar()

    async def update(self, id: int, user: CoreUser) -> Optional[CoreUser]:
        stmt = (
            update(UserModel).
            where(UserModel.id == id).
            values(
                username=user.username,
                email=user.email,
                password_hash=user.hashed_password.value,
                role=user.role,
                is_active=user.is_active
            )
        )
        result = await self._db_session.execute(stmt)

        if result.rowcount == 0:
            await self._db_session.commit()
            return None

        await self._db_session.commit()
        return await self.find_by_id(id)

    async def delete(self, id: int) -> bool:
        stmt = delete(UserModel).where(UserModel.id == id)
        result = await self._db_session.execute(stmt)
        success = result.rowcount > 0
        await self._db_session.commit()
        return success