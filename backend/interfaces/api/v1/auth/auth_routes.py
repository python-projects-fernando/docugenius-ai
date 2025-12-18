from fastapi import APIRouter, Depends, status
from backend.application.dtos.auth_dtos import LoginUserRequest, LoginUserResponse
from backend.application.use_cases.auth.login_user_use_case import LoginUserUseCase
from backend.interfaces.dependencies import get_login_user_use_case
from backend.application.dtos.api_response import APIResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/login",
    response_model=APIResponse[LoginUserResponse],
    status_code=status.HTTP_200_OK,
    summary="Authenticate a user (Login)",
    description="Logs in a user by verifying their credentials (username/email and password). Returns an access token and user information. Version: v1.",
)
async def login_user(
    request_dto: LoginUserRequest,
    use_case: LoginUserUseCase = Depends(get_login_user_use_case)
) -> APIResponse[LoginUserResponse]:
    return await use_case.execute(request_dto=request_dto)