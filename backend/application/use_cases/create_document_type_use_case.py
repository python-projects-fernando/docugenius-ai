from backend.application.repositories.document_type_repository import DocumentTypeRepository
from backend.core.models.document_type import DocumentType
from backend.application.dtos.document_type import CreateDocumentTypeRequest, DocumentTypeResponse
from backend.application.dtos.api_response import APIResponse

class CreateDocumentTypeUseCase:
    def __init__(self, repository: DocumentTypeRepository):
        self._repository = repository

    async def execute(self, request_dto: CreateDocumentTypeRequest) -> APIResponse[DocumentTypeResponse]:
        try:
            existing_doc_type = await self._repository.find_by_name(request_dto.name)
            if existing_doc_type:
                return APIResponse[DocumentTypeResponse](
                    success=False,
                    message="A DocumentType with the given name already exists.",
                    error_code="DUPLICATE_NAME",
                    errors=[f"A DocumentType with the name '{request_dto.name}' already exists."],
                    data=None
                )

            new_doc_type_entity = DocumentType(
                id=None,
                name=request_dto.name,
                description=request_dto.description
            )

            saved_doc_type_entity = await self._repository.save(new_doc_type_entity)

            doc_response_dto = DocumentTypeResponse(
                id=saved_doc_type_entity.id,
                name=saved_doc_type_entity.name,
                description=saved_doc_type_entity.description
            )

            return APIResponse[DocumentTypeResponse](
                success=True,
                message="Document type created successfully.",
                data=doc_response_dto,
                error_code=None,
                errors=None
            )

        except ValueError as ve:
            return APIResponse[DocumentTypeResponse](
                success=False,
                message="Validation error during document creation.",
                error_code="VALIDATION_ERROR",
                errors=[str(ve)],
                data=None
            )

        except Exception as e:
            return APIResponse[DocumentTypeResponse](
                success=False,
                message="An unexpected error occurred during document creation.",
                error_code="CREATE_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )
