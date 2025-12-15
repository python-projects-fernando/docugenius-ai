from backend.application.repositories.document_type_repository import DocumentTypeRepository
from backend.core.models.document_type import DocumentType
from backend.application.dtos.document_type import UpdateDocumentTypeRequest, DocumentTypeResponse
from backend.application.dtos.api_response import APIResponse

class UpdateDocumentTypeUseCase:
    def __init__(self, repository: DocumentTypeRepository):
        self._repository = repository

    async def execute(self, id: int, request_dto: UpdateDocumentTypeRequest) -> APIResponse[DocumentTypeResponse]:
        try:
            existing_doc_type = await self._repository.find_by_id(id)
            if not existing_doc_type:
                return APIResponse[DocumentTypeResponse](
                    success=False,
                    message=f"DocumentType with ID {id} not found.",
                    error_code="NOT_FOUND",
                    errors=[f"DocumentType with ID {id} does not exist."],
                    data=None
                )

            if request_dto.name is not None and request_dto.name != existing_doc_type.name:
                doc_type_with_new_name = await self._repository.find_by_name(request_dto.name)
                if doc_type_with_new_name and doc_type_with_new_name.id != id:
                    return APIResponse[DocumentTypeResponse](
                        success=False,
                        message=f"A DocumentType with the name '{request_dto.name}' already exists.",
                        error_code="DUPLICATE_NAME",
                        errors=[f"A DocumentType with the name '{request_dto.name}' already exists."],
                        data=None
                    )

            updated_doc_type_entity = DocumentType(
                id=existing_doc_type.id,
                name=request_dto.name if request_dto.name is not None else existing_doc_type.name,
                description=request_dto.description if request_dto.description is not None else existing_doc_type.description
            )

            saved_doc_type_entity = await self._repository.update(id, updated_doc_type_entity)

            if saved_doc_type_entity is None:
                 return APIResponse[DocumentTypeResponse](
                    success=False,
                    message=f"Failed to update DocumentType with ID {id}. It may have been deleted.",
                    error_code="UPDATE_FAILED",
                    errors=[f"DocumentType with ID {id} might have been deleted or update failed."],
                    data=None
                )

            doc_response_dto = DocumentTypeResponse(
                id=saved_doc_type_entity.id,
                name=saved_doc_type_entity.name,
                description=saved_doc_type_entity.description
            )

            return APIResponse[DocumentTypeResponse](
                success=True,
                message="Document type updated successfully.",
                data=doc_response_dto,
                error_code=None,
                errors=None
            )

        except ValueError as ve:
            return APIResponse[DocumentTypeResponse](
                success=False,
                message="Validation error during document update.",
                error_code="VALIDATION_ERROR",
                errors=[str(ve)],
                data=None
            )
        except Exception as e:
            return APIResponse[DocumentTypeResponse](
                success=False,
                message="An unexpected error occurred during document update.",
                error_code="UPDATE_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )