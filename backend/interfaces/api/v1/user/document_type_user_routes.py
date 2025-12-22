from fastapi import APIRouter, Depends, status, Query, Path

from backend.application.dtos.document_generation import GenerateDocumentRequest
from backend.application.dtos.document_type import DocumentTypeListResponse, DocumentTypeResponse
from backend.application.dtos.pagination_params import PaginationParams
from backend.application.use_cases.document_type.generate_document_use_case import GenerateDocumentUseCase
from backend.application.use_cases.document_type.get_document_type_by_id_use_case import GetDocumentTypeByIdUseCase
from backend.application.use_cases.document_type.get_document_type_by_name_use_case import GetDocumentTypeByNameUseCase
from backend.application.use_cases.document_type.list_document_types_use_case import ListDocumentTypesUseCase
from backend.core.enums.user_role_enum import UserRole
from backend.core.models.user import User
from backend.interfaces.dependencies import get_list_document_types_use_case, get_get_document_type_by_id_use_case, \
    get_get_document_type_by_name_use_case, role_checker, get_generate_document_use_case
from backend.application.dtos.api_response import APIResponse

router = APIRouter(prefix="/document-types", tags=["Document Types - User/Admin"])

@router.get(
    "/",
    response_model=APIResponse[DocumentTypeListResponse],
    status_code=status.HTTP_200_OK,
    summary="List document types with pagination (User/Admin)",
    description="Lists all available document types with pagination for regular users. Version: v1.",
)
async def list_document_types(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)."),
    size: int = Query(default=10, ge=1, le=100, description="Number of items per page (max 100)."),
    current_user: User = Depends(role_checker([UserRole.COMMON_USER, UserRole.ADMIN])),
    use_case: ListDocumentTypesUseCase = Depends(get_list_document_types_use_case)
) -> APIResponse[DocumentTypeListResponse]:
    pagination_params = PaginationParams(page=page, size=size)
    return await use_case.execute(pagination=pagination_params)


@router.get(
    "/by-id/{id}",
    response_model=APIResponse[DocumentTypeResponse],
    status_code=status.HTTP_200_OK,
    summary="Get a document type by its ID (User/Admin)",
    description="Retrieves details of a specific document type by its unique identifier. Accessible by regular users. Version: v1.",
)
async def get_document_type_by_id(
    id: int = Path(..., title="The ID of the DocumentType to retrieve"),
    current_user: User = Depends(role_checker([UserRole.COMMON_USER, UserRole.ADMIN])),
    use_case: GetDocumentTypeByIdUseCase = Depends(get_get_document_type_by_id_use_case)
) -> APIResponse[DocumentTypeResponse]:
    return await use_case.execute(document_type_id=id)

@router.get(
    "/by-name",
    response_model=APIResponse[DocumentTypeResponse],
    status_code=status.HTTP_200_OK,
    summary="Get a document type by its name (User/Admin)",
    description="Retrieves details of a specific document type by its unique name. Accessible by regular users. Version: v1.",
)
async def get_document_type_by_name(
    name: str = Query(..., title="The name of the DocumentType to retrieve"),
    current_user: User = Depends(role_checker([UserRole.COMMON_USER, UserRole.ADMIN])),
    use_case: GetDocumentTypeByNameUseCase = Depends(get_get_document_type_by_name_use_case)
) -> APIResponse[DocumentTypeResponse]:
    return await use_case.execute(name=name)

@router.post(
    "/generate-document",
    response_model=APIResponse[str],
    status_code=status.HTTP_200_OK,
    summary="Generate a complete document (User/Admin)",
    description="Generates a complete document based on a selected document type and the filled field values provided by the user. Accessible by regular users and administrators. Version: v1.",
)
async def generate_document(
    request_dto: GenerateDocumentRequest,
    current_user: User = Depends(role_checker([UserRole.COMMON_USER, UserRole.ADMIN])),
    use_case: GenerateDocumentUseCase = Depends(get_generate_document_use_case)
) -> APIResponse[str]:
    return await use_case.execute(request_dto=request_dto)