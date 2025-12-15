from backend.application.repositories.document_field_repository import DocumentFieldRepository
from backend.application.repositories.document_type_repository import DocumentTypeRepository
from backend.core.models.document_field import DocumentField as CoreDocumentField
from backend.application.dtos.document_field import CreateDocumentFieldRequest, DocumentFieldResponse
from backend.application.dtos.api_response import APIResponse

class CreateDocumentFieldUseCase:
    def __init__(self, document_field_repository: DocumentFieldRepository, document_type_repository: DocumentTypeRepository):
        self._document_field_repo = document_field_repository
        self._document_type_repo = document_type_repository

    async def execute(self, request_dto: CreateDocumentFieldRequest) -> APIResponse[DocumentFieldResponse]:
        try:
            parent_doc_type = await self._document_type_repo.find_by_id(request_dto.document_type_id)
            if not parent_doc_type:
                return APIResponse[DocumentFieldResponse](
                    success=False,
                    message=f"Parent DocumentType with ID {request_dto.document_type_id} not found.",
                    error_code="PARENT_TYPE_NOT_FOUND",
                    errors=[f"Cannot create field: Parent DocumentType with ID {request_dto.document_type_id} does not exist."],
                    data=None
                )

            existing_field = await self._document_field_repo.find_by_name_and_document_type(
                name=request_dto.name, document_type_id=request_dto.document_type_id
            )
            if existing_field:
                return APIResponse[DocumentFieldResponse](
                    success=False,
                    message=f"A field with the name '{request_dto.name}' already exists for DocumentType ID {request_dto.document_type_id}.",
                    error_code="DUPLICATE_FIELD_NAME_IN_TYPE",
                    errors=[f"Field name '{request_dto.name}' is already used in this DocumentType."],
                    data=None
                )

            new_doc_field_entity = CoreDocumentField(
                id=None,
                document_type_id=request_dto.document_type_id,
                name=request_dto.name,
                field_type=request_dto.field_type,
                is_required=request_dto.is_required,
                description=request_dto.description
            )

            saved_doc_field_entity = await self._document_field_repo.save(new_doc_field_entity)

            doc_field_response_dto = DocumentFieldResponse(
                id=saved_doc_field_entity.id,
                document_type_id=saved_doc_field_entity.document_type_id,
                name=saved_doc_field_entity.name,
                field_type=saved_doc_field_entity.field_type,
                is_required=saved_doc_field_entity.is_required,
                description=saved_doc_field_entity.description
            )

            return APIResponse[DocumentFieldResponse](
                success=True,
                message="Document field created successfully.",
                data=doc_field_response_dto,
                error_code=None,
                errors=None
            )

        except ValueError as ve:
            return APIResponse[DocumentFieldResponse](
                success=False,
                message="Validation error during document field creation.",
                error_code="VALIDATION_ERROR",
                errors=[str(ve)],
                data=None
            )
        except Exception as e:
            return APIResponse[DocumentFieldResponse](
                success=False,
                message="An unexpected error occurred during document field creation.",
                error_code="CREATE_FIELD_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )