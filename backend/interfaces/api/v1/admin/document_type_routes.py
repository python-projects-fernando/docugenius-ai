from typing import List

from fastapi import APIRouter, Depends, status, Path
from backend.application.dtos.document_type import CreateDocumentTypeRequest, DocumentTypeResponse, \
    UpdateDocumentTypeRequest, DeleteDocumentTypeResponse
from backend.application.dtos.document_type_suggestion import GenerateDocumentTypesResponse, \
    GenerateDocumentTypesRequest
from backend.application.dtos.enum_dtos import EnumListResponse
from backend.application.use_cases.document_type.batch_create_document_types_use_case import \
    BatchCreateDocumentTypesUseCase
from backend.application.use_cases.document_type.create_document_type_use_case import CreateDocumentTypeUseCase
from backend.application.use_cases.document_type.delete_document_type_use_case import DeleteDocumentTypeUseCase
from backend.application.use_cases.document_type.suggest_document_types_use_case import SuggestDocumentTypesUseCase
from backend.application.use_cases.document_type.update_document_type_use_case import UpdateDocumentTypeUseCase
from backend.application.use_cases.enum.get_field_types_use_case import GetFieldTypesUseCase
from backend.interfaces.dependencies import get_create_document_type_use_case, get_update_document_type_use_case, \
    get_delete_document_type_use_case, get_batch_create_document_types_use_case, \
    get_suggest_document_types_use_case, get_get_field_types_use_case
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


@router.post(
    "/batch-create",
    response_model=APIResponse[List[DocumentTypeResponse]],
    status_code=status.HTTP_201_CREATED,
    summary="Create multiple document types in a batch (Admin)",
    description="Creates multiple new document types in a single request. Access restricted to administrators. Version: v1.",
)
async def batch_create_document_types(
    request_dtos: List[CreateDocumentTypeRequest],
    use_case: BatchCreateDocumentTypesUseCase = Depends(get_batch_create_document_types_use_case)
) -> APIResponse[List[DocumentTypeResponse]]:
    return await use_case.execute(request_dtos=request_dtos)


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


@router.delete(
    "/{id}",
    response_model=APIResponse[DeleteDocumentTypeResponse],
    status_code=status.HTTP_200_OK,
    summary="Delete an existing document type (Admin)",
    description="Deletes an existing document type by its ID. Access restricted to administrators. Version: v1.",
)
async def delete_document_type(
    id: int = Path(..., title="The ID of the DocumentType to delete"),
    use_case: DeleteDocumentTypeUseCase = Depends(get_delete_document_type_use_case)
) -> APIResponse[DeleteDocumentTypeResponse]:
    return await use_case.execute(id=id)


@router.post(
    "/suggest",
    response_model=APIResponse[GenerateDocumentTypesResponse],
    status_code=status.HTTP_200_OK,
    summary="Suggest document types based on business description (Admin)",
    description="Calls the AI to suggest common document types for a given business description. Access restricted to administrators. Version: v1.",
)
async def suggest_document_types(
    request_dto: GenerateDocumentTypesRequest,
    use_case: SuggestDocumentTypesUseCase = Depends(get_suggest_document_types_use_case)
) -> APIResponse[GenerateDocumentTypesResponse]:
    return await use_case.execute(request_dto=request_dto)

