from pydantic import BaseModel, Field
from typing import Optional, List
from backend.core.enums.field_type_enum import FieldType


class CreateDocumentFieldRequest(BaseModel):
    document_type_id: int = Field(..., description="The ID of the DocumentType this field belongs to.")
    name: str = Field(..., description="The name of the field (e.g., 'company_name', 'service_value').", min_length=1)
    field_type: FieldType = Field(...,description="The type of the field, mapped to HTML input types or concepts (e.g., text, integer, decimal, textarea, select).")
    is_required: bool = Field(False, description="Whether the field is required or not.")
    description: Optional[str] = Field(None, description="An optional description of the field's purpose.")



class UpdateDocumentFieldRequest(BaseModel):
    name: Optional[str] = Field(None, description="The updated display name of the field (e.g., 'Updated Company Name').", min_length=1)
    type: Optional[str] = Field(None, description="The updated type of the field "
                                                  "(e.g., 'text', 'integer', 'decimal', 'textarea', 'select'). "
                                                  "Must correspond to HTML input types or specific conventions like "
                                                  "'integer'/'decimal'.")
    required: Optional[bool] = Field(None, description="Whether the field is mandatory or optional.")
    description: Optional[str] = Field(None, description="An optional updated description of the field's purpose.")



class DocumentFieldResponse(BaseModel):
    id: Optional[int] = Field(..., description="The unique identifier of the document field. Can be None if not persisted yet.")
    document_type_id: int = Field(..., description="The ID of the DocumentType this field belongs to.")
    name: str = Field(..., description="The name of the field (e.g., 'company_name', 'service_value').")
    field_type: FieldType = Field(..., description="The type of the field (e.g., text, integer, decimal, textarea, select).")
    is_required: bool = Field(..., description="Whether the field is required or not.")
    description: Optional[str] = Field(None, description="An optional description of the field's purpose.")

    class Config:
        from_attributes = True


class CreateDocumentFieldRequestForBatch(BaseModel):
    name: str = Field(
        ...,
        description="The display name of the field (e.g., 'Contracting Company', 'Service Value', 'Start Date'). Used as a label in the form.",
        min_length=1
    )
    type: FieldType = Field(
        ...,
        description="The type of the field, using the FieldType Enum (e.g., text, integer, decimal, textarea, select, radio, checkbox, date, email)."
    )
    required: bool = Field(
        False,
        description="Whether the field is mandatory (True) or optional (False). Defaults to False."
    )
    description: str = Field(
        ...,
        description="A brief description explaining the purpose or expected content of the field.",
        min_length=1
    )

    def __post_init__(self):
        self.name = self.name.strip()
        self.description = self.description.strip()


class BatchCreateDocumentFieldsRequest(BaseModel):
    document_type_id: int = Field(
        ...,
        gt=0,
        description="The ID of the DocumentType to which all the fields in this batch belong. Must be a positive integer."
    )
    fields: List[CreateDocumentFieldRequestForBatch] = Field(
        ...,
        min_length=1,
        description="The list of fields to be created for the specified DocumentType. Must contain at least one field definition."
    )


class DocumentFieldListResponse(BaseModel):
    items: List[DocumentFieldResponse] = Field(..., description="The list of DocumentField items.")