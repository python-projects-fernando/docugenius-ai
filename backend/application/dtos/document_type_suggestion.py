from pydantic import BaseModel
from typing import List

class GenerateDocumentTypesRequest(BaseModel):
    business_description: str

class SuggestedDocumentType(BaseModel):
    name: str
    description: str

class GenerateDocumentTypesResponse(BaseModel):
    suggested_document_types: List[SuggestedDocumentType]