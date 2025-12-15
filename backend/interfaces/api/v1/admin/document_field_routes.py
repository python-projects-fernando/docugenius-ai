from fastapi import APIRouter, Depends, status
from backend.application.dtos.document_field import CreateDocumentFieldRequest, DocumentFieldResponse
from backend.application.use_cases.document_field.create_document_field_use_case import CreateDocumentFieldUseCase
from backend.interfaces.dependencies import get_create_document_field_use_case
from backend.application.dtos.api_response import APIResponse

router = APIRouter(prefix="/document-fields", tags=["Document Fields - Admin"])

@router.post(
    "/",
    response_model=APIResponse[DocumentFieldResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new document field (Admin)",
    description="Creates a new field definition for a specific document type. Access restricted to administrators. Version: v1.",
)
async def create_document_field(
    request_dto: CreateDocumentFieldRequest,
    use_case: CreateDocumentFieldUseCase = Depends(get_create_document_field_use_case)
) -> APIResponse[DocumentFieldResponse]:
    return await use_case.execute(request_dto=request_dto)