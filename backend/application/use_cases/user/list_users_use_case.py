from typing import List as TypingList
import math

from backend.application.repositories.user_repository import UserRepository
from backend.core.models.user import User as CoreUser
from backend.application.dtos.user import UserResponse, UserListResponse
from backend.application.dtos.pagination_params import PaginationParams
from backend.application.dtos.api_response import APIResponse

class ListUsersUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def execute(self, pagination: PaginationParams) -> APIResponse[UserListResponse]:
        try:
            offset = (pagination.page - 1) * pagination.size
            items_core = await self._repository.find_all_paginated(offset=offset, limit=pagination.size)
            total = await self._repository.count_all()
            total_pages = math.ceil(total / pagination.size) if total > 0 else 0

            items_response_dto = [
                UserResponse(
                    id=entity.id,
                    username=entity.username,
                    email=entity.email,
                    role=entity.role,
                    is_active=entity.is_active,
                    created_at=entity.created_at,
                    updated_at=entity.updated_at
                )
                for entity in items_core
            ]

            list_response_dto = UserListResponse(
                items=items_response_dto,
                total=total,
                page=pagination.page,
                size=pagination.size,
                pages=total_pages
            )

            return APIResponse[UserListResponse](
                success=True,
                message="Users retrieved successfully.",
                data=list_response_dto,
                error_code=None,
                errors=None
            )

        except Exception as e:
            return APIResponse[UserListResponse](
                success=False,
                message="An unexpected error occurred while retrieving users.",
                error_code="LIST_USERS_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )