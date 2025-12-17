from typing import List
from backend.application.repositories.document_field_repository import DocumentFieldRepository
from backend.application.repositories.document_type_repository import DocumentTypeRepository
from backend.core.models.document_field import DocumentField as CoreDocumentField
from backend.core.models.document_type import DocumentType as CoreDocumentType
from backend.application.dtos.document_field import BatchCreateDocumentFieldsRequest, CreateDocumentFieldRequestForBatch
from backend.application.dtos.document_field import DocumentFieldResponse
from backend.application.dtos.api_response import APIResponse

class BatchCreateDocumentFieldsUseCase:
    def __init__(self, document_type_repo: DocumentTypeRepository, document_field_repo: DocumentFieldRepository):
        self._document_type_repo = document_type_repo
        self._document_field_repo = document_field_repo

    async def execute(self, request_dto: BatchCreateDocumentFieldsRequest) -> APIResponse[List[DocumentFieldResponse]]:
        try:
            parent_doc_type: CoreDocumentType = await self._document_type_repo.find_by_id(request_dto.document_type_id)
            if not parent_doc_type:
                return APIResponse[List[DocumentFieldResponse]](
                    success=False,
                    message=f"Parent DocumentType with ID {request_dto.document_type_id} not found.",
                    error_code="PARENT_DOC_TYPE_NOT_FOUND",
                    errors=[f"Cannot create fields: Parent DocumentType with ID {request_dto.document_type_id} does not exist."],
                    data=None
                )

            created_fields = []
            errors_occurred = False
            error_messages = []

            for field_request_item in request_dto.fields:
                try:
                    existing_field = await self._document_field_repo.find_by_name_and_document_type(
                        name=field_request_item.name, document_type_id=request_dto.document_type_id
                    )
                    if existing_field:
                        error_msg = f"A field with the name '{field_request_item.name}' already exists for DocumentType ID {request_dto.document_type_id}."
                        error_messages.append(error_msg)
                        errors_occurred = True
                        continue

                    new_field_entity = CoreDocumentField(
                        id=None,
                        document_type_id=request_dto.document_type_id,
                        name=field_request_item.name,
                        field_type=field_request_item.type,
                        is_required=field_request_item.required,
                        description=field_request_item.description
                    )

                    saved_field_entity = await self._document_field_repo.save(new_field_entity)

                    field_response_dto = DocumentFieldResponse(
                        id=saved_field_entity.id,
                        document_type_id=saved_field_entity.document_type_id,
                        name=saved_field_entity.name,
                        field_type=saved_field_entity.field_type,
                        is_required=saved_field_entity.is_required,
                        description=saved_field_entity.description
                    )

                    created_fields.append(field_response_dto)

                except ValueError as ve:
                    error_msg = f"Validation error for field '{field_request_item.name}': {str(ve)}"
                    error_messages.append(error_msg)
                    errors_occurred = True
                    continue
                except Exception as e:
                    error_msg = f"Error creating field '{field_request_item.name}': {str(e)}"
                    error_messages.append(error_msg)
                    errors_occurred = True
                    continue

            if errors_occurred:
                return APIResponse[List[DocumentFieldResponse]](
                    success=False,
                    message="Some document fields failed to be created during batch operation.",
                    error_code="BATCH_CREATE_FIELDS_PARTIAL_ERROR",
                    errors=error_messages,
                    data=created_fields
                )

            return APIResponse[List[DocumentFieldResponse]](
                success=True,
                message=f"Successfully created {len(created_fields)} fields for DocumentType ID {request_dto.document_type_id}.",
                data=created_fields,
                error_code=None,
                errors=None
            )

        except Exception as e:
            return APIResponse[List[DocumentFieldResponse]](
                success=False,
                message="An unexpected error occurred during batch document field creation.",
                error_code="BATCH_CREATE_FIELDS_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )