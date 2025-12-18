import bcrypt
import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from backend.application.repositories.user_repository import UserRepository
from backend.core.models.user import User as CoreUser
from backend.application.dtos.auth_dtos import LoginUserRequest, LoginUserResponse
from backend.application.dtos.user import UserResponse
from backend.application.dtos.api_response import APIResponse

class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self._user_repo = user_repository
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
        self.JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")
        if not self.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY environment variable not set.")
        if not self.JWT_REFRESH_SECRET_KEY:
            raise ValueError("JWT_REFRESH_SECRET_KEY environment variable not set.")

        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
        self.REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

    async def execute(self, request_dto: LoginUserRequest) -> APIResponse[LoginUserResponse]:
        try:
            user_entity: CoreUser = await self._user_repo.find_by_username(request_dto.identifier)
            if not user_entity:
                user_entity = await self._user_repo.find_by_email(request_dto.identifier)

            if not user_entity:
                return APIResponse[LoginUserResponse](
                    success=False,
                    message="Invalid credentials.",
                    error_code="INVALID_CREDENTIALS",
                    errors=["Username or email not found."],
                    data=None
                )

            if not user_entity.is_active:
                return APIResponse[LoginUserResponse](
                    success=False,
                    message="Account is inactive.",
                    error_code="INACTIVE_ACCOUNT",
                    errors=["This account has been deactivated."],
                    data=None
                )

            is_password_valid = bcrypt.checkpw(
                request_dto.password.encode('utf-8'),
                hashed_password=user_entity.hashed_password.value.encode('utf-8')
            )

            if not is_password_valid:
                return APIResponse[LoginUserResponse](
                    success=False,
                    message="Invalid credentials.",
                    error_code="INVALID_CREDENTIALS",
                    errors=["Incorrect password."],
                    data=None
                )

            access_token_expires_delta = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token_exp = datetime.now(timezone.utc) + access_token_expires_delta
            access_token_payload = {
                "sub": str(user_entity.id),
                "username": user_entity.username,
                "email": user_entity.email,
                "role": user_entity.role.value,
                "exp": int(access_token_exp.timestamp()),
                "type": "access"
            }
            access_token = jwt.encode(access_token_payload, self.JWT_SECRET_KEY, algorithm="HS256")

            refresh_token_expires_delta = timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)
            refresh_token_exp = datetime.now(timezone.utc) + refresh_token_expires_delta
            refresh_token_payload = {
                "sub": str(user_entity.id),
                "exp": int(refresh_token_exp.timestamp()),
                "type": "refresh"
            }
            refresh_token = jwt.encode(refresh_token_payload, self.JWT_REFRESH_SECRET_KEY, algorithm="HS256")

            user_response_dto = UserResponse(
                id=user_entity.id,
                username=user_entity.username,
                email=user_entity.email,
                role=user_entity.role,
                is_active=user_entity.is_active,
                created_at=user_entity.created_at,
                updated_at=user_entity.updated_at
            )

            login_response_dto = LoginUserResponse(
                access_token=access_token,
                user=user_response_dto.model_dump()
            )

            return APIResponse[LoginUserResponse](
                success=True,
                message="Login successful.",
                data=login_response_dto,
                error_code=None,
                errors=None
            )

        except JWTError as je:
            return APIResponse[LoginUserResponse](
                success=False,
                message="An error occurred during token generation.",
                error_code="TOKEN_GENERATION_ERROR",
                errors=[f"JWT encoding error: {str(je)}"],
                data=None
            )
        except Exception as e:
            return APIResponse[LoginUserResponse](
                success=False,
                message="An unexpected error occurred during login.",
                error_code="LOGIN_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )