from backend.application.repositories.document_type_repository import DocumentTypeRepository
from backend.core.models.document_type import DocumentType
from backend.application.dtos.document_type import DocumentTypeResponse
from backend.application.dtos.api_response import APIResponse

class GetDocumentTypeByNameUseCase:
    def __init__(self, repository: DocumentTypeRepository):
        self._repository = repository

    async def execute(self, name: str) -> APIResponse[DocumentTypeResponse]:
        try:
            doc_type_entity = await self._repository.find_by_name(name)

            if not doc_type_entity:
                return APIResponse[DocumentTypeResponse](
                    success=False,
                    message=f"DocumentType with name '{name}' not found.",
                    error_code="NOT_FOUND",
                    errors=[f"DocumentType with name '{name}' does not exist."],
                    data=None
                )

            doc_type_response_dto = DocumentTypeResponse(
                id=doc_type_entity.id,
                name=doc_type_entity.name,
                description=doc_type_entity.description
            )

            return APIResponse[DocumentTypeResponse](
                success=True,
                message="Document type retrieved successfully.",
                data=doc_type_response_dto,
                error_code=None,
                errors=None
            )

        except Exception as e:
            return APIResponse[DocumentTypeResponse](
                success=False,
                message="An unexpected error occurred while retrieving the document type.",
                error_code="GET_DT_BY_NAME_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )