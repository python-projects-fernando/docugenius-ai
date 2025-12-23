import bcrypt
import secrets
import string
import logging
from backend.application.repositories.user_repository import UserRepository
from backend.core.models.user import User as CoreUser
from backend.core.value_objects.hashed_password import HashedPassword
from backend.application.dtos.user import CreateUserRequest, UserResponse
from backend.application.dtos.api_response import APIResponse
from backend.application.email.email import EmailGateway
import redis.asyncio as redis

logger = logging.getLogger(__name__)

class CreateUserUseCase:
    def __init__(self, repository: UserRepository, email_gateway: EmailGateway, redis_client: redis.Redis):
        self._repository = repository
        self._email_gateway = email_gateway
        self._redis_client = redis_client

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

            temp_password_length = 12
            alphabet = string.ascii_letters + string.digits
            temp_password = ''.join(secrets.choice(alphabet) for _ in range(temp_password_length))
            print(f"Temporary password generated for {request_dto.username}: {temp_password}")

            password_hash_bytes = bcrypt.hashpw(temp_password.encode('utf-8'), bcrypt.gensalt())
            password_hash_str = password_hash_bytes.decode('utf-8')
            hashed_password_vo = HashedPassword(value=password_hash_str)

            new_user_entity = CoreUser(
                id=None,
                username=request_dto.username,
                email=str(request_dto.email),
                hashed_password=hashed_password_vo,
                role=request_dto.role,
                is_active=False
            )

            saved_user_entity = await self._repository.save(new_user_entity)

            reset_token = secrets.token_urlsafe(32)
            redis_key = f"reset_token:{reset_token}"
            user_id_str = str(saved_user_entity.id)
            token_ttl_seconds = 3600

            await self._redis_client.setex(redis_key, token_ttl_seconds, user_id_str)

            base_url = "http://localhost:8000"
            reset_link = f"{base_url}/api/v1/auth/reset-password?token={reset_token}"

            email_subject = "Set Your Password for DocuGenius-AI"
            email_body = f"""
            Hello {request_dto.username},

            An account has been created for you on DocuGenius-AI.
            Please click the link below to set your password:

            {reset_link}

            This link will expire in 1 hour.

            If you did not request this, please ignore this email.

            Best regards,
            DocuGenius-AI Team
            """

            email_sent_success = await self._email_gateway.send_email(
                to_email=request_dto.email,
                subject=email_subject,
                body=email_body
            )

            if not email_sent_success:
                print(f"Warning: Failed to send email to {request_dto.email}")

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
                message="User created successfully. A password reset email has been sent.",
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
            logger.error(f"Error during user creation: {e}")
            return APIResponse[UserResponse](
                success=False,
                message="An unexpected error occurred during user creation.",
                error_code="CREATE_USER_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )