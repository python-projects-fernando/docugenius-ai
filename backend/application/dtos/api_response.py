from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar, List

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    success: bool = Field(..., description="Indicates if the request was successful (True) or failed (False).")
    message: str = Field(..., description="A human-readable message providing information about the result of the request.")
    data: Optional[T] = Field(None, description="The main data payload of the response. Present if 'success' is True and data is available.")
    error_code: Optional[str] = Field(None, description="A specific error code identifying the type of error, if any occurred (e.g., 'DOC_TYPE_NOT_FOUND'). Present if 'success' is False.")
    errors: Optional[List[str]] = Field(None, description="A list of detailed error messages, if any occurred. Present if 'success' is False.")

# APIResponse[DocumentTypeResponse](success=True, message="Document created", data=doc_response_dto)
# APIResponse[DocumentTypeResponse](success=False, message="Document creation error", error_code="CREATE_ERROR", errors=["Name is mandatory"])