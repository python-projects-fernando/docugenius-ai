from pydantic import BaseModel
from typing import Dict, Any

class GenerateDocumentRequest(BaseModel):
    document_type_id: int
    filled_fields: Dict[str, Any]

# class GenerateDocumentResponse(BaseModel):
#     """
#     DTO for the response containing the generated document or a link to it.
#     """
#     download_link: str
#