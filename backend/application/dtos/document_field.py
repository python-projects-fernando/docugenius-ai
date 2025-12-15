from pydantic import BaseModel, Field
from typing import Optional

class CreateDocumentFieldRequest(BaseModel):
    document_type_id: int = Field(..., description="The ID of the DocumentType this field belongs to.")
    name: str = Field(..., description="The name of the field (e.g., 'company_name', 'service_value').", min_length=1)
    field_type: str = Field(..., description="The data type of the field (e.g., 'string', 'integer', 'date', 'boolean', 'text').", min_length=1)
    is_required: bool = Field(False, description="Whether the field is required or not.")
    description: Optional[str] = Field(None, description="An optional description of the field's purpose.")


class DocumentFieldResponse(BaseModel):
    id: Optional[int] = Field(..., description="The unique identifier of the document field. Can be None if not persisted yet.")
    document_type_id: int = Field(..., description="The ID of the DocumentType this field belongs to.")
    name: str = Field(..., description="The name of the field (e.g., 'company_name', 'service_value').")
    field_type: str = Field(..., description="The data type of the field (e.g., 'string', 'integer', 'date', 'boolean', 'text').")
    is_required: bool = Field(..., description="Whether the field is required or not.")
    description: Optional[str] = Field(None, description="An optional description of the field's purpose.")

    class Config:
        from_attributes = True