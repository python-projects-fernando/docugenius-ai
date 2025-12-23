from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.sql import func
from backend.infrastructure.models.base import Base
from backend.core.enums.user_role_enum import UserRole

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.COMMON_USER)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    def __repr__(self) -> str:
        return (f"<UserModel(id={self.id}, username='{self.username}', email='{self.email}', role={self.role}, "
                f"is_active={self.is_active}, created_at={self.created_at}, "
                f"updated_at={self.updated_at}, created_by_user_id={self.created_by_user_id}, "
                f"updated_by_user_id={self.updated_by_user_id})>")