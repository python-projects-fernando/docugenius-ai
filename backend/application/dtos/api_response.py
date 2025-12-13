from pydantic import BaseModel
from typing import Optional, Generic, TypeVar, List

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    error_code: Optional[str] = None
    errors: Optional[List[str]] = None

# APIResponse[DocumentTypeResponse](success=True, message="Document created", data=doc_response_dto)
# APIResponse[DocumentTypeResponse](success=False, message="Document creation error", error_code="CREATE_ERROR", errors=["Name is mandatory"])