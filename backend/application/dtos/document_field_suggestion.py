from pydantic import BaseModel
from typing import List
from backend.core.enums.field_type_enum import FieldType

class SuggestedDocumentField(BaseModel):
    name: str
    type: FieldType
    required: bool
    description: str

class GenerateDocumentFieldsRequest(BaseModel):
    document_type_name: str
    document_type_description: str

class GenerateDocumentFieldsResponse(BaseModel):
    document_type: str
    description: str
    fields: List[SuggestedDocumentField]