from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number (1-indexed).")
    size: int = Field(default=10, ge=1, le=100, description="Number of items per page (max 100).")