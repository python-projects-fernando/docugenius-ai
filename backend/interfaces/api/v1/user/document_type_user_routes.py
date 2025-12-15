from fastapi import APIRouter, Depends, status, Query
from backend.application.dtos.document_type import PaginationParams, DocumentTypeListResponse
from backend.application.use_cases.list_document_types_use_case import ListDocumentTypesUseCase
from backend.interfaces.dependencies import get_list_document_types_use_case
from backend.application.dtos.api_response import APIResponse

router = APIRouter(prefix="/document-types", tags=["Document Types - User"])

@router.get(
    "/",
    response_model=APIResponse[DocumentTypeListResponse],
    status_code=status.HTTP_200_OK,
    summary="List document types with pagination (User)",
    description="Lists all available document types with pagination for regular users. Version: v1.",
)
async def list_document_types(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)."),
    size: int = Query(default=10, ge=1, le=100, description="Number of items per page (max 100)."),
    use_case: ListDocumentTypesUseCase = Depends(get_list_document_types_use_case)
) -> APIResponse[DocumentTypeListResponse]:
    pagination_params = PaginationParams(page=page, size=size)
    return await use_case.execute(pagination=pagination_params)