from fastapi import APIRouter, Depends, status, Path, Query
from backend.application.dtos.user import CreateUserRequest, UserResponse, UpdateUserRequest
from backend.application.use_cases.user.create_user_use_case import CreateUserUseCase
from backend.application.use_cases.user.delete_user_use_case import DeleteUserUseCase
from backend.application.use_cases.user.get_user_by_id_use_case import GetUserByIdUseCase
from backend.application.use_cases.user.get_user_by_username_use_case import GetUserByUsernameUseCase
from backend.application.use_cases.user.update_user_use_case import UpdateUserUseCase
from backend.interfaces.dependencies import get_create_user_use_case, get_update_user_use_case, \
    get_delete_user_use_case, get_get_user_by_id_use_case, get_get_user_by_username_use_case
from backend.application.dtos.api_response import APIResponse

router = APIRouter(prefix="/users", tags=["Users - Admin"])

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


@router.delete(
    "/{id}",
    response_model=APIResponse[bool],
    status_code=status.HTTP_200_OK,
    summary="Delete an existing user (Admin)",
    description="Deletes an existing user. Access restricted to administrators. Version: v1.",
)
async def delete_user(
    id: int = Path(..., title="The ID of the User to delete"),
    use_case: DeleteUserUseCase = Depends(get_delete_user_use_case)
) -> APIResponse[bool]:
    return await use_case.execute(user_id=id)

@router.get(
    "/by-id/{id}",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get a user by its ID (Admin)",
    description="Retrieves details of a specific user by its unique identifier. Access restricted to administrators. Version: v1.",
)
async def get_user_by_id(
    id: int = Path(..., title="The ID of the User to retrieve"),
    use_case: GetUserByIdUseCase = Depends(get_get_user_by_id_use_case)
) -> APIResponse[UserResponse]:
    return await use_case.execute(user_id=id)

@router.get(
    "/by-username",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get a user by its username (Admin)",
    description="Retrieves details of a specific user by its unique username. Access restricted to administrators. Version: v1.",
)
async def get_user_by_username(
    username: str = Query(..., title="The username of the User to retrieve"),
    use_case: GetUserByUsernameUseCase = Depends(get_get_user_by_username_use_case)
) -> APIResponse[UserResponse]:
    return await use_case.execute(username=username)