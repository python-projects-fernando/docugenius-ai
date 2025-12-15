import bcrypt
from backend.application.repositories.user_repository import UserRepository
from backend.core.models.user import User as CoreUser
from backend.core.value_objects.hashed_password import HashedPassword
from backend.application.dtos.user import CreateUserRequest, UserResponse
from backend.application.dtos.api_response import APIResponse

class CreateUserUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def execute(self, request_dto: CreateUserRequest) -> APIResponse[UserResponse]:
        try:
            existing_user_by_username = await self._repository.find_by_username(request_dto.username)
            if existing_user_by_username:
                return APIResponse[UserResponse](
                    success=False,
                    message=f"A User with the username '{request_dto.username}' already exists.",
                    error_code="DUPLICATE_USERNAME",
                    errors=[f"Username '{request_dto.username}' is already taken."],
                    data=None
                )

            existing_user_by_email = await self._repository.find_by_email(request_dto.email)
            if existing_user_by_email:
                return APIResponse[UserResponse](
                    success=False,
                    message=f"A User with the email '{request_dto.email}' already exists.",
                    error_code="DUPLICATE_EMAIL",
                    errors=[f"Email '{request_dto.email}' is already registered."],
                    data=None
                )

            password_hash_bytes = bcrypt.hashpw(request_dto.password.encode('utf-8'), bcrypt.gensalt())
            password_hash_str = password_hash_bytes.decode('utf-8')
            hashed_password_vo = HashedPassword(value=password_hash_str)

            new_user_entity = CoreUser(
                id=None,
                username=request_dto.username,
                email=request_dto.email,
                hashed_password=hashed_password_vo,
            )

            saved_user_entity = await self._repository.save(new_user_entity)

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
                message="User created successfully.",
                data=user_response_dto,
                error_code=None,
                errors=None
            )

        except ValueError as ve:
            return APIResponse[UserResponse](
                success=False,
                message="Validation error during user creation.",
                error_code="VALIDATION_ERROR",
                errors=[str(ve)],
                data=None
            )
        except Exception as e:
            return APIResponse[UserResponse](
                success=False,
                message="An unexpected error occurred during user creation.",
                error_code="CREATE_USER_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )