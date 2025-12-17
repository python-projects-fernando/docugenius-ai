from backend.application.repositories.document_field_repository import DocumentFieldRepository
from backend.core.models.document_field import DocumentField as CoreDocumentField
from backend.application.dtos.document_field import DocumentFieldResponse
from backend.application.dtos.api_response import APIResponse

class GetDocumentFieldByIdUseCase:
    def __init__(self, repository: DocumentFieldRepository):
        self._repository = repository

    async def execute(self, field_id: int) -> APIResponse[DocumentFieldResponse]:
        try:
            field_entity: CoreDocumentField = await self._repository.find_by_id(field_id)

            if not field_entity:
                return APIResponse[DocumentFieldResponse](
                    success=False,
                    message=f"DocumentField with ID {field_id} not found.",
                    error_code="FIELD_NOT_FOUND",
                    errors=[f"DocumentField with ID {field_id} does not exist."],
                    data=None
                )

            field_response_dto = DocumentFieldResponse(
                id=field_entity.id,
                document_type_id=field_entity.document_type_id,
                name=field_entity.name,
                field_type=field_entity.field_type,
                is_required=field_entity.is_required,
                description=field_entity.description
            )

            return APIResponse[DocumentFieldResponse](
                success=True,
                message="Document field retrieved successfully.",
                data=field_response_dto,
                error_code=None,
                errors=None
            )

        except Exception as e:
            return APIResponse[DocumentFieldResponse](
                success=False,
                message="An unexpected error occurred during document field retrieval.",
                error_code="GET_FIELD_BY_ID_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )