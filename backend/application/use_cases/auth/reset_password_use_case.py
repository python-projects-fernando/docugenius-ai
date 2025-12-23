import bcrypt
import logging
from backend.application.repositories.user_repository import UserRepository
from backend.application.dtos.auth_dtos import ResetPasswordRequest
from backend.application.dtos.api_response import APIResponse
from backend.core.models.user import User as CoreUser
from backend.core.value_objects.hashed_password import HashedPassword
import redis.asyncio as redis

logger = logging.getLogger(__name__)

class ResetPasswordUseCase:
    def __init__(self, user_repository: UserRepository, redis_client: redis.Redis):
        self._user_repository = user_repository
        self._redis_client = redis_client

    async def execute(self, request_dto: ResetPasswordRequest) -> APIResponse[dict]:
        try:
            token = request_dto.token
            new_password = request_dto.new_password

            redis_key = f"reset_token:{token}"
            user_id_str = await self._redis_client.get(redis_key)

            if not user_id_str:
                return APIResponse[dict](
                    success=False,
                    message="Invalid or expired reset token.",
                    error_code="INVALID_TOKEN",
                    errors=["The provided reset token is invalid or has expired."],
                    data=None
                )

            try:
                user_id = int(user_id_str)
            except ValueError:
                logger.error(f"Invalid user ID format retrieved from Redis for token {token}: {user_id_str}")
                return APIResponse[dict](
                    success=False,
                    message="An error for password reset.",
                    error_code="REDIS_DATA_ERROR",
                    errors=["An internal error occurred while processing the token."],
                    data=None
                )

            user_entity: CoreUser = await self._user_repository.find_by_id(user_id)
            if not user_entity:
                logger.warning(f"User with ID {user_id} not found for reset token {token}")
                return APIResponse[dict](
                    success=False,
                    message="User associated with this token was not found.",
                    error_code="USER_NOT_FOUND",
                    errors=["The user account associated with this reset link no longer exists."],
                    data=None
                )

            password_hash_bytes = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            password_hash_str = password_hash_bytes.decode('utf-8')
            new_hashed_password_vo = HashedPassword(value=password_hash_str)

            print(
                f"[DEBUG] ResetPasswordUseCase: Generated new hash: {new_hashed_password_vo.value[:10]}...")
            print(
                f"[DEBUG] ResetPasswordUseCase: User entity before update - ID: {user_entity.id}, "
                f"Hash: {user_entity.hashed_password.value[:10]}..., "
                f"Role: {user_entity.role}, "
                f"IsActive: {user_entity.is_active}")

            user_entity.hashed_password = new_hashed_password_vo
            user_entity.is_active = True

            updated_user_entity = await self._user_repository.update(user_entity)
            print(
                f"[DEBUG] ResetPasswordUseCase: Updated entity returned - "
                f"ID: {updated_user_entity.id if updated_user_entity else 'None'}, "
                f"Hash: {updated_user_entity.hashed_password.value[:10] if updated_user_entity and updated_user_entity.hashed_password else 'None'}..., Role: {updated_user_entity.role if updated_user_entity else 'None'}, IsActive: {updated_user_entity.is_active if updated_user_entity else 'None'}")

            if not updated_user_entity:
                 logger.warning(f"Failed to update user with ID {user_id} during password reset.")
                 return APIResponse[dict](
                    success=False,
                    message="Failed to update user password.",
                    error_code="UPDATE_FAILED",
                    errors=["An error occurred while updating your password. Please try again."],
                    data=None
                 )

            await self._redis_client.delete(redis_key)

            return APIResponse[dict](
                success=True,
                message="Password reset successfully.",
                data=None,
                error_code=None,
                errors=None
            )

        except Exception as e:
            logger.error(f"Error during password reset: {e}")
            return APIResponse[dict](
                success=False,
                message="An unexpected error occurred during password reset.",
                error_code="RESET_PASSWORD_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )