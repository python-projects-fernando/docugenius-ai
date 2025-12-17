from backend.application.repositories.document_field_repository import DocumentFieldRepository
from backend.application.dtos.api_response import APIResponse

class DeleteDocumentFieldUseCase:
    def __init__(self, repository: DocumentFieldRepository):
        self._repository = repository

    async def execute(self, field_id: int) -> APIResponse[bool]:
        try:
            existing_field = await self._repository.find_by_id(field_id)
            if not existing_field:
                return APIResponse[bool](
                    success=False,
                    message=f"DocumentField with ID {field_id} not found.",
                    error_code="FIELD_NOT_FOUND",
                    errors=[f"Cannot delete field: DocumentField with ID {field_id} does not exist."],
                    data=False
                )

            success = await self._repository.delete(field_id)

            if success:
                return APIResponse[bool](
                    success=True,
                    message="Document field deleted successfully.",
                    data=True,
                    error_code=None,
                    errors=None
                )
            else:
                return APIResponse[bool](
                    success=False,
                    message=f"Failed to delete DocumentField with ID {field_id}. It may have been deleted concurrently or an internal error occurred.",
                    error_code="DELETE_FAILED_CONCURRENT_OR_INTERNAL",
                    errors=[f"DocumentField with ID {field_id} might have been deleted concurrently or delete operation failed internally."],
                    data=False
                )

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error during document field deletion: {e}")
            return APIResponse[bool](
                success=False,
                message="An unexpected error occurred during document field deletion.",
                error_code="DELETE_FIELD_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=False
            )