from fastapi import APIRouter, Depends, status, Query, Path
from backend.application.dtos.document_type import PaginationParams, DocumentTypeListResponse, DocumentTypeResponse
from backend.application.use_cases.document_type.get_document_type_by_id_use_case import GetDocumentTypeByIdUseCase
from backend.application.use_cases.document_type.get_document_type_by_name_use_case import GetDocumentTypeByNameUseCase
from backend.application.use_cases.document_type.list_document_types_use_case import ListDocumentTypesUseCase
from backend.interfaces.dependencies import get_list_document_types_use_case, get_get_document_type_by_id_use_case, \
    get_get_document_type_by_name_use_case
from backend.application.dtos.api_response import APIResponse

router = APIRouter(prefix="/document-types", tags=["User - Document Types"])

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


@router.get(
    "/by-id/{id}",
    response_model=APIResponse[DocumentTypeResponse],
    status_code=status.HTTP_200_OK,
    summary="Get a document type by its ID (User)",
    description="Retrieves details of a specific document type by its unique identifier. Accessible by regular users. Version: v1.",
)
async def get_document_type_by_id(
    id: int = Path(..., title="The ID of the DocumentType to retrieve"),
    use_case: GetDocumentTypeByIdUseCase = Depends(get_get_document_type_by_id_use_case)
) -> APIResponse[DocumentTypeResponse]:
    return await use_case.execute(document_type_id=id)

@router.get(
    "/by-name",
    response_model=APIResponse[DocumentTypeResponse],
    status_code=status.HTTP_200_OK,
    summary="Get a document type by its name (User)",
    description="Retrieves details of a specific document type by its unique name. Accessible by regular users. Version: v1.",
)
async def get_document_type_by_name(
    name: str = Query(..., title="The name of the DocumentType to retrieve"),
    use_case: GetDocumentTypeByNameUseCase = Depends(get_get_document_type_by_name_use_case)
) -> APIResponse[DocumentTypeResponse]:
    return await use_case.execute(name=name)