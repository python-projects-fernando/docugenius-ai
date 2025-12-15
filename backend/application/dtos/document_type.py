from pydantic import BaseModel, Field
from typing import Optional, List

class CreateDocumentTypeRequest(BaseModel):
    name: str = Field(..., description="The name of the document type (e.g., 'Service Contract').", min_length=1)
    description: Optional[str] = Field(None, description="An optional description of the document type.")


class UpdateDocumentTypeRequest(BaseModel):
    name: Optional[str] = Field(None, description="The updated name of the document type.", min_length=1)
    description: Optional[str] = Field(None, description="An optional updated description of the document type.")


class DocumentTypeResponse(BaseModel):
    id: Optional[int] = Field(..., description="The unique identifier of the document type. Can be None if not persisted yet.")
    name: str = Field(..., description="The name of the document type (e.g., 'Service Contract').")
    description: Optional[str] = Field(None, description="An optional description of the document type.")

    class Config:
        from_attributes = True


class DeleteDocumentTypeResponse(BaseModel):
    message: str = Field(..., description="Confirmation message of the deletion.")
    deleted_id: int = Field(..., description="The ID of the deleted DocumentType.")


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number (1-indexed).")
    size: int = Field(default=10, ge=1, le=100, description="Number of items per page (max 100).")


class DocumentTypeListResponse(BaseModel):
    items: List[DocumentTypeResponse] = Field(..., description="The list of DocumentType items for the current page.")
    total: int = Field(..., description="The total number of items available.")
    page: int = Field(..., description="The current page number (1-indexed).")
    size: int = Field(..., description="The number of items per page.")
    pages: int = Field(..., description="The total number of pages available.")