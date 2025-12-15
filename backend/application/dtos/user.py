from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class CreateUserRequest(BaseModel):
    username: str = Field(..., description="The unique username for the new user.", min_length=1, max_length=80)
    email: EmailStr = Field(..., description="The email address for the new user.")
    password: str = Field(..., description="The plain text password for the new user.", min_length=8)

class UserResponse(BaseModel):
    id: Optional[int] = Field(..., description="The unique identifier of the user. Can be None if not persisted yet.")
    username: str = Field(..., description="The unique username of the user.")
    email: str = Field(..., description="The email address of the user.")
    role: str = Field(..., description="The role of the user (e.g., 'admin', 'common').")
    is_active: bool = Field(..., description="Whether the user account is active.")
    created_at: Optional[datetime] = Field(None, description="Timestamp of user creation.")
    updated_at: Optional[datetime] = Field(None, description="Timestamp of last user update.")

    class Config:
        from_attributes = True