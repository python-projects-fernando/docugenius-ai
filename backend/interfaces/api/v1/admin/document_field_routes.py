from typing import List

from fastapi import APIRouter, Depends, status, Path
from backend.application.dtos.document_field import CreateDocumentFieldRequest, DocumentFieldResponse, \
    BatchCreateDocumentFieldsRequest, DocumentFieldListResponse, UpdateDocumentFieldRequest
from backend.application.dtos.document_field_suggestion import GenerateDocumentFieldsResponse, \
    GenerateDocumentFieldsRequest
from backend.application.use_cases.document_field.batch_create_document_fields_use_case import \
    BatchCreateDocumentFieldsUseCase
from backend.application.use_cases.document_field.create_document_field_use_case import CreateDocumentFieldUseCase
from backend.application.use_cases.document_field.delete_document_field_use_case import DeleteDocumentFieldUseCase
from backend.application.use_cases.document_field.get_document_field_by_id_use_case import GetDocumentFieldByIdUseCase
from backend.application.use_cases.document_field.list_document_fields_by_document_type_use_case import \
    ListDocumentFieldsByDocumentTypeUseCase
from backend.application.use_cases.document_field.suggest_document_fields_use_case import SuggestDocumentFieldsUseCase
from backend.application.use_cases.document_field.update_document_field_use_case import UpdateDocumentFieldUseCase
from backend.application.use_cases.document_type.suggest_document_types_use_case import SuggestDocumentTypesUseCase
from backend.interfaces.dependencies import get_create_document_field_use_case, get_suggest_document_fields_use_case, \
    get_batch_create_document_fields_use_case, get_list_document_fields_by_document_type_use_case, \
    get_get_document_field_by_id_use_case, get_update_document_field_use_case, get_delete_document_field_use_case
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
    "/batch-create",
    response_model=APIResponse[List[DocumentFieldResponse]],
    status_code=status.HTTP_201_CREATED,
    summary="Create multiple document fields in a batch (Admin)",
    description="Creates multiple new document fields for a specific document type in a single request. Access restricted to administrators. Version: v1.",
)
async def batch_create_document_fields(
    request_dto: BatchCreateDocumentFieldsRequest,
    use_case: BatchCreateDocumentFieldsUseCase = Depends(get_batch_create_document_fields_use_case)
) -> APIResponse[List[DocumentFieldResponse]]:
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

@router.get(
    "/{id}",
    response_model=APIResponse[DocumentFieldResponse],
    status_code=status.HTTP_200_OK,
    summary="Get a specific document field by ID (Admin)",
    description="Retrieves the details of a single document field identified by its unique ID. Access restricted to administrators. Version: v1.",
)
async def get_document_field_by_id(
    id: int = Path(..., title="The ID of the DocumentField to retrieve"),
    use_case: GetDocumentFieldByIdUseCase = Depends(get_get_document_field_by_id_use_case)
) -> APIResponse[DocumentFieldResponse]:
    return await use_case.execute(field_id=id)


@router.get(
    "/by-document-type/{document_type_id}",
    response_model=APIResponse[DocumentFieldListResponse],
    status_code=status.HTTP_200_OK,
    summary="List fields for a specific document type (Admin)",
    description="Retrieves all fields associated with a given document type ID. Access restricted to administrators. Version: v1.",
)
async def list_document_fields_by_document_type(
    document_type_id: int = Path(..., title="The ID of the DocumentType to list fields for"),
    use_case: ListDocumentFieldsByDocumentTypeUseCase = Depends(get_list_document_fields_by_document_type_use_case)
) -> APIResponse[DocumentFieldListResponse]:
    return await use_case.execute(document_type_id=document_type_id)

@router.put(
    "/{id}",
    response_model=APIResponse[DocumentFieldResponse],
    status_code=status.HTTP_200_OK,
    summary="Update a specific document field by ID (Admin)",
    description="Updates the details of a single document field identified by its unique ID. Access restricted to administrators. Version: v1.",
)
async def update_document_field(
    id: int = Path(..., title="The ID of the DocumentField to update"),
    request_dto: UpdateDocumentFieldRequest = ...,
    use_case: UpdateDocumentFieldUseCase = Depends(get_update_document_field_use_case)
) -> APIResponse[DocumentFieldResponse]:
    return await use_case.execute(field_id=id, request_dto=request_dto)

@router.delete(
    "/{id}",
    response_model=APIResponse[bool],
    status_code=status.HTTP_200_OK,
    summary="Delete a specific document field by ID (Admin)",
    description="Deletes a single document field identified by its unique ID. Access restricted to administrators. Version: v1.",
)
async def delete_document_field(
    id: int = Path(..., title="The ID of the DocumentField to delete"),
    use_case: DeleteDocumentFieldUseCase = Depends(get_delete_document_field_use_case)
) -> APIResponse[bool]:
    return await use_case.execute(field_id=id)