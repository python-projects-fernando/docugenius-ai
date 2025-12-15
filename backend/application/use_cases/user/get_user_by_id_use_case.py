from backend.application.repositories.user_repository import UserRepository
from backend.core.models.user import User as CoreUser
from backend.application.dtos.user import UserResponse
from backend.application.dtos.api_response import APIResponse

class GetUserByIdUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def execute(self, user_id: int) -> APIResponse[UserResponse]:
        try:
            user_entity = await self._repository.find_by_id(user_id)

            if not user_entity:
                return APIResponse[UserResponse](
                    success=False,
                    message=f"User with ID {user_id} not found.",
                    error_code="USER_NOT_FOUND",
                    errors=[f"User with ID {user_id} does not exist."],
                    data=None
                )

            user_response_dto = UserResponse(
                id=user_entity.id,
                username=user_entity.username,
                email=user_entity.email,
                role=user_entity.role,
                is_active=user_entity.is_active,
                created_at=user_entity.created_at,
                updated_at=user_entity.updated_at
            )

            return APIResponse[UserResponse](
                success=True,
                message="User retrieved successfully.",
                data=user_response_dto,
                error_code=None,
                errors=None
            )

        except Exception as e:
            return APIResponse[UserResponse](
                success=False,
                message="An unexpected error occurred while retrieving the user.",
                error_code="GET_USER_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )