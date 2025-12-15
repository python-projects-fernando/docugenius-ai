from fastapi import APIRouter, Depends, status, Path
from backend.application.dtos.user import CreateUserRequest, UserResponse, UpdateUserRequest
from backend.application.use_cases.user.create_user_use_case import CreateUserUseCase
from backend.application.use_cases.user.update_user_use_case import UpdateUserUseCase
from backend.interfaces.dependencies import get_create_user_use_case, get_update_user_use_case
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


@router.put(
    "/{id}",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Update an existing user (Admin)",
    description="Updates an existing user's profile information (excluding password). Access restricted to administrators. Version: v1.",
)
async def update_user(
    id: int = Path(..., title="The ID of the User to update"),
    request_dto: UpdateUserRequest = ...,
    use_case: UpdateUserUseCase = Depends(get_update_user_use_case)
) -> APIResponse[UserResponse]:
    return await use_case.execute(user_id=id, request_dto=request_dto)