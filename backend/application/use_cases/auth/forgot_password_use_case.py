import logging
import secrets
import os
from backend.application.repositories.user_repository import UserRepository
from backend.application.email.email import EmailGateway
from backend.application.dtos.auth_dtos import ForgotPasswordRequest
from backend.application.dtos.api_response import APIResponse
import redis.asyncio as redis

logger = logging.getLogger(__name__)

class ForgotPasswordUseCase:
    def __init__(self, user_repository: UserRepository, email_gateway: EmailGateway, redis_client: redis.Redis):
        self._user_repository = user_repository
        self._email_gateway = email_gateway
        self._redis_client = redis_client
        self._base_url = os.getenv("BASE_URL", "http://localhost:8000")

    async def execute(self, request_dto: ForgotPasswordRequest) -> APIResponse[dict]:
        try:
            email = request_dto.email

            user_entity = await self._user_repository.find_by_email(email)
            if not user_entity:
                logger.info(f"Forgot password request for non-existent email: {email}")
                return APIResponse[dict](
                    success=True,
                    message="If the email address is associated with an account, a password reset link has been sent.",
                    data=None,
                    error_code=None,
                    errors=None
                )

            reset_token = secrets.token_urlsafe(32)

            redis_key = f"reset_token:{reset_token}"
            user_id_str = str(user_entity.id)
            token_ttl_seconds = 3600

            await self._redis_client.setex(redis_key, token_ttl_seconds, user_id_str)

            reset_link = f"{self._base_url}/api/v1/auth/reset-password?token={reset_token}"

            email_subject = "Reset Your Password for DocuGenius-AI"
            email_body = f"""
            Hello {user_entity.username},

            You have requested to reset your password on DocuGenius-AI.
            Please click the link below to set a new password:

            {reset_link}

            This link will expire in 1 hour.

            If you did not request this, please ignore this email.

            Best regards,
            DocuGenius-AI Team
            """

            email_sent_success = await self._email_gateway.send_email(
                to_email=email,
                subject=email_subject,
                body=email_body
            )

            if not email_sent_success:
                logger.warning(f"Failed to send password reset email to {email}")

            return APIResponse[dict](
                success=True,
                message="If the email address is associated with an account, a password reset link has been sent.",
                data=None,
                error_code=None,
                errors=None
            )

        except Exception as e:
            logger.error(f"Error during forgot password request: {e}")
            return APIResponse[dict](
                success=False,
                message="An unexpected error occurred during the forgot password request.",
                error_code="FORGOT_PASSWORD_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )