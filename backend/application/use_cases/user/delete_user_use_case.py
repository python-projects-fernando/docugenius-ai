from backend.application.repositories.user_repository import UserRepository
from backend.application.dtos.api_response import APIResponse

class DeleteUserUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def execute(self, user_id: int) -> APIResponse[bool]:
        try:
            existing_user = await self._repository.find_by_id(user_id)
            if not existing_user:
                return APIResponse[bool](
                    success=False,
                    message=f"User with ID {user_id} not found.",
                    error_code="USER_NOT_FOUND",
                    errors=[f"Cannot delete user: User with ID {user_id} does not exist."],
                    data=False
                )

            success = await self._repository.delete(user_id)

            if success:
                return APIResponse[bool](
                    success=True,
                    message="User deleted successfully.",
                    error_code=None,
                    errors=None,
                    data=True
                )
            else:
                return APIResponse[bool](
                    success=False,
                    message=f"Failed to delete User with ID {user_id}. It may have been deleted concurrently.",
                    error_code="DELETE_FAILED",
                    errors=[f"User with ID {user_id} might have been deleted concurrently or delete failed."],
                    data=False
                )

        except Exception as e:
            return APIResponse[bool](
                success=False,
                message="An unexpected error occurred during user deletion.",
                error_code="DELETE_USER_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=False
            )