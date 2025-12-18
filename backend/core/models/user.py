from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone

from backend.core.enums.user_role_enum import UserRole
from backend.core.value_objects.hashed_password import HashedPassword

@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    hashed_password: HashedPassword
    role: UserRole = UserRole.COMMON_USER
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by_user_id: Optional[int] = None

    def __post_init__(self):
        if not self.username or not self.username.strip():
            raise ValueError("User username cannot be empty or just whitespace.")
        if not self.email or not self.email.strip():
            raise ValueError("User email cannot be empty or just whitespace.")
        if not isinstance(self.role, UserRole):
            raise ValueError(f"User role must be a member of UserRole Enum. Got: {type(self.role)}, value: {self.role}")

        self.username = self.username.strip()
        self.email = self.email.strip()

        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)

        if self.updated_at is None:
            self.updated_at = datetime.now(timezone.utc)

    def set_password(self, password_hash_value: str):
        if not password_hash_value:
            raise ValueError("Password hash cannot be empty")
        new_hashed_password = HashedPassword(value=password_hash_value)
        self.hashed_password = new_hashed_password
        self.updated_at = datetime.now(timezone.utc)


    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        if self.id is not None and other.id is not None:
            return self.id == other.id
        return (
            self.username == other.username
            and self.email == other.email
            and self.hashed_password == other.hashed_password
            and self.role == other.role
            and self.is_active == other.is_active
        )

    def __hash__(self):
        if self.id is not None:
            return hash(self.id)
        return hash((self.username, self.email, self.hashed_password, self.role, self.is_active))


    def __repr__(self):
        return (f"User(id={self.id}, username='{self.username}', email='{self.email}', role={self.role}, "
                f"is_active={self.is_active}, created_at={self.created_at}, updated_at={self.updated_at}, "
                f"created_by_user_id={self.created_by_user_id})")