from fastapi import APIRouter, Depends, status
from backend.application.dtos.user import CreateUserRequest, UserResponse
from backend.application.use_cases.user.create_user_use_case import CreateUserUseCase
from backend.interfaces.dependencies import get_create_user_use_case
from backend.application.dtos.api_response import APIResponse

router = APIRouter(prefix="/users", tags=["Admin - Users"])

@router.post(
    "/",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user (Admin)",
    description="Creates a new user. Access restricted to administrators. Version: v1.",
)
async def create_user(
    request_dto: CreateUserRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case)
) -> APIResponse[UserResponse]:
    return await use_case.execute(request_dto=request_dto)