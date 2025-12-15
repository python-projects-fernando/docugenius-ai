from backend.application.repositories.document_type_repository import DocumentTypeRepository
from backend.application.dtos.document_type import DeleteDocumentTypeResponse
from backend.application.dtos.api_response import APIResponse

class DeleteDocumentTypeUseCase:
    def __init__(self, repository: DocumentTypeRepository):
        self._repository = repository

    async def execute(self, id: int) -> APIResponse[DeleteDocumentTypeResponse]:
        try:
            existing_doc_type = await self._repository.find_by_id(id)
            if not existing_doc_type:
                return APIResponse[DeleteDocumentTypeResponse](
                    success=False,
                    message=f"DocumentType with ID {id} not found.",
                    error_code="NOT_FOUND",
                    errors=[f"DocumentType with ID {id} does not exist."],
                    data=None
                )

            success = await self._repository.delete(id)

            if not success:
                return APIResponse[DeleteDocumentTypeResponse](
                    success=False,
                    message=f"Failed to delete DocumentType with ID {id}.",
                    error_code="DELETE_FAILED",
                    errors=[f"An error occurred while deleting DocumentType with ID {id}."],
                    data=None
                )

            delete_response_dto = DeleteDocumentTypeResponse(
                message=f"DocumentType with ID {id} deleted successfully.",
                deleted_id=id
            )

            return APIResponse[DeleteDocumentTypeResponse](
                success=True,
                message="Document type deleted successfully.",
                data=delete_response_dto,
                error_code=None,
                errors=None
            )

        except Exception as e:
            return APIResponse[DeleteDocumentTypeResponse](
                success=False,
                message="An unexpected error occurred during document deletion.",
                error_code="DELETE_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )