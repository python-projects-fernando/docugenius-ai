from typing import Protocol, Optional, List
from backend.core.models.user import User


class UserRepository(Protocol):
    async def save(self, user: User, created_by_user_id: int = None) -> User:
        ...

    async def find_by_id(self, id: int) -> Optional[User]:
        ...

    async def find_by_username(self, username: str) -> Optional[User]:
        ...

    async def find_by_email(self, email: str) -> Optional[User]:
        ...

    async def find_all(self) -> List[User]:
        ...

    async def find_all_paginated(self, offset: int, limit: int) -> List[User]:
        ...

    async def count_all(self) -> int:
        ...

    async def update(self, user: User) -> Optional[User]:
        ...

    async def delete(self, id: int) -> bool:
        ...