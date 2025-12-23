from fastapi import APIRouter, Depends, status, Path, Query

from backend.application.dtos.enum_dtos import EnumListResponse
from backend.application.dtos.user import CreateUserRequest, UserResponse, UpdateUserRequest, UserListResponse
from backend.application.dtos.pagination_params import PaginationParams
from backend.application.use_cases.enum.get_user_roles_use_case import GetUserRolesUseCase
from backend.application.use_cases.user.create_user_use_case import CreateUserUseCase
from backend.application.use_cases.user.delete_user_use_case import DeleteUserUseCase
from backend.application.use_cases.user.get_user_by_email_use_case import GetUserByEmailUseCase
from backend.application.use_cases.user.get_user_by_id_use_case import GetUserByIdUseCase
from backend.application.use_cases.user.get_user_by_username_use_case import GetUserByUsernameUseCase
from backend.application.use_cases.user.list_users_use_case import ListUsersUseCase
from backend.application.use_cases.user.update_user_use_case import UpdateUserUseCase
from backend.core.enums.user_role_enum import UserRole
from backend.core.models.user import User
from backend.interfaces.dependencies import get_create_user_use_case, get_update_user_use_case, \
    get_delete_user_use_case, get_get_user_by_id_use_case, get_get_user_by_username_use_case, \
    get_get_user_by_email_use_case, get_list_users_use_case, get_get_user_roles_use_case, \
    role_checker
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
    current_user: User = Depends(role_checker([UserRole.ADMIN])),
    use_case: CreateUserUseCase = Depends(get_create_user_use_case)
) -> APIResponse[UserResponse]:
    return await use_case.execute(request_dto=request_dto, created_by_user_id=current_user.id)


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
    current_user: User = Depends(role_checker([UserRole.ADMIN])),
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
    current_user: User = Depends(role_checker([UserRole.ADMIN])),
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
    current_user: User = Depends(role_checker([UserRole.ADMIN])),
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
    current_user: User = Depends(role_checker([UserRole.ADMIN])),
    use_case: GetUserByUsernameUseCase = Depends(get_get_user_by_username_use_case)
) -> APIResponse[UserResponse]:
    return await use_case.execute(username=username)

@router.get(
    "/by-email",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get a user by its email (Admin)",
    description="Retrieves details of a specific user by its unique email address. Access restricted to administrators. Version: v1.",
)
async def get_user_by_email(
    email: str = Query(..., title="The email of the User to retrieve"),
    current_user: User = Depends(role_checker([UserRole.ADMIN])),
    use_case: GetUserByEmailUseCase = Depends(get_get_user_by_email_use_case)
) -> APIResponse[UserResponse]:
    return await use_case.execute(email=email)

@router.get(
    "/",
    response_model=APIResponse[UserListResponse],
    status_code=status.HTTP_200_OK,
    summary="List users with pagination (Admin)",
    description="Lists all users with pagination. Access restricted to administrators. Version: v1.",
)
async def list_users(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)."),
    size: int = Query(default=10, ge=1, le=100, description="Number of items per page (max 100)."),
    ccurrent_user: User = Depends(role_checker([UserRole.ADMIN])),
    use_case: ListUsersUseCase = Depends(get_list_users_use_case)
) -> APIResponse[UserListResponse]:
    pagination_params = PaginationParams(page=page, size=size)
    return await use_case.execute(pagination=pagination_params)

@router.get(
    "/user-roles",
    response_model=APIResponse[EnumListResponse],
    status_code=status.HTTP_200_OK,
    summary="List available user roles (Admin)",
    description="Returns a list of all valid user roles (e.g., admin, common) that can be assigned to users. Access restricted to administrators. Version: v1.",
)
async def list_user_roles(
    current_user: User = Depends(role_checker([UserRole.ADMIN])),
    use_case: GetUserRolesUseCase = Depends(get_get_user_roles_use_case)
) -> APIResponse[EnumListResponse]:
    return await use_case.execute()