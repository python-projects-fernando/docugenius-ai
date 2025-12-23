from backend.application.repositories.user_repository import UserRepository
from backend.core.models.user import User as CoreUser
from backend.application.dtos.user import UpdateUserRequest, UserResponse
from backend.application.dtos.api_response import APIResponse

class UpdateUserUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def execute(self, user_id: int, request_dto: UpdateUserRequest, updated_by_user_id: int) -> APIResponse[UserResponse]:
        try:
            existing_user = await self._repository.find_by_id(user_id)
            if not existing_user:
                return APIResponse[UserResponse](
                    success=False,
                    message=f"User with ID {user_id} not found.",
                    error_code="USER_NOT_FOUND",
                    errors=[f"User with ID {user_id} does not exist."],
                    data=None
                )

            updated_username = request_dto.username if request_dto.username is not None else existing_user.username
            updated_email = request_dto.email if request_dto.email is not None else existing_user.email
            updated_role = request_dto.role if request_dto.role is not None else existing_user.role
            updated_is_active = request_dto.is_active if request_dto.is_active is not None else existing_user.is_active

            if updated_username != existing_user.username:
                user_with_new_username = await self._repository.find_by_username(updated_username)
                if user_with_new_username and user_with_new_username.id != user_id:
                    return APIResponse[UserResponse](
                        success=False,
                        message=f"A User with the username '{updated_username}' already exists.",
                        error_code="DUPLICATE_USERNAME",
                        errors=[f"Username '{updated_username}' is already taken."],
                        data=None
                    )

            if updated_email != existing_user.email:
                user_with_new_email = await self._repository.find_by_email(updated_email)
                if user_with_new_email and user_with_new_email.id != user_id:
                    return APIResponse[UserResponse](
                        success=False,
                        message=f"A User with the email '{updated_email}' already exists.",
                        error_code="DUPLICATE_EMAIL",
                        errors=[f"Email '{updated_email}' is already registered."],
                        data=None
                    )

            updated_user_entity = CoreUser(
                id=existing_user.id,
                username=updated_username,
                email=updated_email,
                hashed_password=existing_user.hashed_password,
                role=updated_role,
                is_active=updated_is_active,
                created_at=existing_user.created_at,
            )

            saved_user_entity = await self._repository.update(updated_user_entity, updated_by_user_id=updated_by_user_id)

            if saved_user_entity is None:
                 return APIResponse[UserResponse](
                    success=False,
                    message=f"Failed to update User with ID {user_id}. It may have been deleted.",
                    error_code="UPDATE_FAILED",
                    errors=[f"User with ID {user_id} might have been deleted or update failed."],
                    data=None
                )

            user_response_dto = UserResponse(
                id=saved_user_entity.id,
                username=saved_user_entity.username,
                email=saved_user_entity.email,
                role=saved_user_entity.role,
                is_active=saved_user_entity.is_active,
                created_at=saved_user_entity.created_at,
                updated_at=saved_user_entity.updated_at
            )

            return APIResponse[UserResponse](
                success=True,
                message="User updated successfully.",
                data=user_response_dto,
                error_code=None,
                errors=None
            )

        except ValueError as ve:
            return APIResponse[UserResponse](
                success=False,
                message="Validation error during user update.",
                error_code="VALIDATION_ERROR",
                errors=[str(ve)],
                data=None
            )
        except Exception as e:
            return APIResponse[UserResponse](
                success=False,
                message="An unexpected error occurred during user update.",
                error_code="UPDATE_USER_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )