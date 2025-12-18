from pydantic import BaseModel, Field
from typing import List

class GenerateDocumentTypesRequest(BaseModel):
    business_description: str = Field(
        ...,
        description="A brief description of the business or sector to suggest document types for (e.g., 'Law firm specializing in labor law').",
        min_length=1
    )

    def __post_init__(self):
        self.business_description = self.business_description.strip()

class SuggestedDocumentType(BaseModel):
    name: str = Field(
        ...,
        description="The name of the suggested document type (e.g., 'Service Contract', 'Commercial Proposal', 'Employment Agreement').",
        min_length=1
    )
    description: str = Field(
        ...,
        description="A brief description of the document type and its purpose within the business context.",
        min_length=1
    )

    def __post_init__(self):
        self.name = self.name.strip()
        self.description = self.description.strip()

class GenerateDocumentTypesResponse(BaseModel):
    suggested_document_types: List[SuggestedDocumentType] = Field(
        ...,
        description="The list of document types suggested by the AI based on the business description."
    )