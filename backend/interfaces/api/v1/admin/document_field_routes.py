from fastapi import APIRouter, Depends, status
from backend.application.dtos.document_field import CreateDocumentFieldRequest, DocumentFieldResponse
from backend.application.dtos.document_field_suggestion import GenerateDocumentFieldsResponse, \
    GenerateDocumentFieldsRequest
from backend.application.use_cases.document_field.create_document_field_use_case import CreateDocumentFieldUseCase
from backend.application.use_cases.document_field.suggest_document_fields_use_case import SuggestDocumentFieldsUseCase
from backend.application.use_cases.document_type.suggest_document_types_use_case import SuggestDocumentTypesUseCase
from backend.interfaces.dependencies import get_create_document_field_use_case, get_suggest_document_fields_use_case
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


@router.post(
    "/suggest",
    response_model=APIResponse[GenerateDocumentFieldsResponse],
    status_code=status.HTTP_200_OK,
    summary="Suggest fields for a new document type (Admin)",
    description="Calls the AI to suggest essential fields for a given document type based on its name and description. Access restricted to administrators. Version: v1.",
)
async def suggest_document_fields(
    request_dto: GenerateDocumentFieldsRequest,
    use_case: SuggestDocumentFieldsUseCase = Depends(get_suggest_document_fields_use_case)
) -> APIResponse[GenerateDocumentFieldsResponse]:
    return await use_case.execute(request_dto=request_dto)