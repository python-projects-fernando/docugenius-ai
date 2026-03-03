from fastapi import APIRouter, Depends, status, Path

from backend.application.dtos.api_response import APIResponse
from backend.application.dtos.document_field import DocumentFieldListResponse
from backend.application.use_cases.document_field.list_document_fields_by_document_type_use_case import \
    ListDocumentFieldsByDocumentTypeUseCase
from backend.core.enums.user_role_enum import UserRole
from backend.core.models.user import User
from backend.interfaces.dependencies import get_list_document_fields_by_document_type_use_case, role_checker



router = APIRouter(prefix="/document-fields", tags=["Document Fields - User/Admin"])

@router.get(
    "/by-document-type/{document_type_id}",
    response_model=APIResponse[DocumentFieldListResponse],
    status_code=status.HTTP_200_OK,
    summary="List fields for a specific document type (Admin)",
    description="Retrieves all fields associated with a given document type ID. Accessible by regular users and administrators. Version: v1.",
)
async def list_document_fields_by_document_type(
    document_type_id: int = Path(..., title="The ID of the DocumentType to list fields for"),
    current_user: User = Depends(role_checker([UserRole.COMMON_USER, UserRole.ADMIN])),
    use_case: ListDocumentFieldsByDocumentTypeUseCase = Depends(get_list_document_fields_by_document_type_use_case)
) -> APIResponse[DocumentFieldListResponse]:
    return await use_case.execute(document_type_id=document_type_id)