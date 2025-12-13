from fastapi import APIRouter, Depends, status, Path
from backend.application.dtos.document_type import CreateDocumentTypeRequest, DocumentTypeResponse, \
    UpdateDocumentTypeRequest
from backend.application.use_cases.create_document_type_use_case import CreateDocumentTypeUseCase
from backend.application.use_cases.update_document_type_use_case import UpdateDocumentTypeUseCase
from backend.interfaces.dependencies import get_create_document_type_use_case, get_update_document_type_use_case
from backend.application.dtos.api_response import APIResponse

router = APIRouter(prefix="/document-types", tags=["Document Types - Admin"])


@router.post(
    "/",
    response_model=APIResponse[DocumentTypeResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new document type (Admin)",
    description="Creates a new document type. Access restricted to administrators. Version: v1.",
)
async def create_document_type(
    request_dto: CreateDocumentTypeRequest,
    use_case: CreateDocumentTypeUseCase = Depends(get_create_document_type_use_case)
) -> APIResponse[DocumentTypeResponse]:
    return await use_case.execute(request_dto)


@router.put(
    "/{id}",
    response_model=APIResponse[DocumentTypeResponse],
    status_code=status.HTTP_200_OK,
    summary="Update an existing document type (Admin)",
    description="Updates an existing document type by its ID. Access restricted to administrators. Version: v1.",
)
async def update_document_type(
    id: int = Path(..., title="The ID of the DocumentType to update"),
    request_dto: UpdateDocumentTypeRequest = ...,
    use_case: UpdateDocumentTypeUseCase = Depends(get_update_document_type_use_case)
) -> APIResponse[DocumentTypeResponse]:
    return await use_case.execute(id=id, request_dto=request_dto)