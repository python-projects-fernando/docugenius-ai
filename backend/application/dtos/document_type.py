from pydantic import BaseModel, Field
from typing import Optional

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