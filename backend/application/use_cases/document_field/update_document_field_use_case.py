from backend.application.repositories.document_field_repository import DocumentFieldRepository
from backend.application.repositories.document_type_repository import DocumentTypeRepository
from backend.core.models.document_field import DocumentField as CoreDocumentField
from backend.core.enums.field_type_enum import FieldType
from backend.application.dtos.document_field import UpdateDocumentFieldRequest, DocumentFieldResponse
from backend.application.dtos.api_response import APIResponse

class UpdateDocumentFieldUseCase:
    def __init__(self, document_field_repo: DocumentFieldRepository, document_type_repo: DocumentTypeRepository):
        self._document_field_repo = document_field_repo
        self._document_type_repo = document_type_repo

    async def execute(self, field_id: int, request_dto: UpdateDocumentFieldRequest) -> APIResponse[DocumentFieldResponse]:
        try:
            existing_field_entity: CoreDocumentField = await self._document_field_repo.find_by_id(field_id)
            if not existing_field_entity:
                return APIResponse[DocumentFieldResponse](
                    success=False,
                    message=f"DocumentField with ID {field_id} not found.",
                    error_code="FIELD_NOT_FOUND",
                    errors=[f"Cannot update field: DocumentField with ID {field_id} does not exist."],
                    data=None
                )

            document_type_id = existing_field_entity.document_type_id

            if request_dto.name is not None and request_dto.name != existing_field_entity.name:
                 conflicting_field = await self._document_field_repo.find_by_name_and_document_type(
                     name=request_dto.name, document_type_id=document_type_id
                 )
                 if conflicting_field and conflicting_field.id != field_id:
                     return APIResponse[DocumentFieldResponse](
                         success=False,
                         message=f"A field with the name '{request_dto.name}' already exists for DocumentType ID {document_type_id}.",
                         error_code="DUPLICATE_FIELD_NAME_IN_TYPE",
                         errors=[f"Field name '{request_dto.name}' is already used in this DocumentType."],
                         data=None
                     )

            updated_name = request_dto.name if request_dto.name is not None else existing_field_entity.name
            updated_type_enum = existing_field_entity.field_type
            if request_dto.type is not None:
                try:
                    if request_dto.type.lower() == "integer":
                        updated_type_enum = FieldType.INTEGER
                    elif request_dto.type.lower() == "decimal":
                        updated_type_enum = FieldType.DECIMAL
                    else:
                        updated_type_enum = FieldType(request_dto.type.upper())
                except (ValueError, AttributeError):
                    return APIResponse[DocumentFieldResponse](
                        success=False,
                        message="Invalid field type provided.",
                        error_code="INVALID_FIELD_TYPE",
                        errors=[f"Field type '{request_dto.type}' is not valid."],
                        data=None
                    )

            updated_required = request_dto.required if request_dto.required is not None else existing_field_entity.is_required
            updated_description = request_dto.description if request_dto.description is not None else existing_field_entity.description

            updated_field_entity = CoreDocumentField(
                id=existing_field_entity.id,
                document_type_id=existing_field_entity.document_type_id,
                name=updated_name,
                field_type=updated_type_enum,
                is_required=updated_required,
                description=updated_description
            )

            saved_field_entity = await self._document_field_repo.update(field_id, updated_field_entity)

            if saved_field_entity is None:
                 return APIResponse[DocumentFieldResponse](
                    success=False,
                    message=f"Failed to update DocumentField with ID {field_id}. It may have been deleted concurrently.",
                    error_code="UPDATE_FAILED",
                    errors=[f"DocumentField with ID {field_id} might have been deleted or update failed."],
                    data=None
                )

            field_response_dto = DocumentFieldResponse(
                id=saved_field_entity.id,
                document_type_id=saved_field_entity.document_type_id,
                name=saved_field_entity.name,
                field_type=saved_field_entity.field_type,
                is_required=saved_field_entity.is_required,
                description=saved_field_entity.description
            )

            return APIResponse[DocumentFieldResponse](
                success=True,
                message="Document field updated successfully.",
                data=field_response_dto,
                error_code=None,
                errors=None
            )

        except ValueError as ve:
            return APIResponse[DocumentFieldResponse](
                success=False,
                message="Validation error during document field update.",
                error_code="VALIDATION_ERROR",
                errors=[str(ve)],
                data=None
            )
        except Exception as e:
            return APIResponse[DocumentFieldResponse](
                success=False,
                message="An unexpected error occurred during document field update.",
                error_code="UPDATE_FIELD_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )