from backend.core.enums.user_role_enum import UserRole
from backend.application.dtos.enum_dtos import EnumValue, EnumListResponse
from backend.application.dtos.api_response import APIResponse

class GetUserRolesUseCase:
    async def execute(self) -> APIResponse[EnumListResponse]:
        user_role_values = [EnumValue(name=member.name, value=member.value) for member in UserRole]

        response_data = EnumListResponse(
            enum_name="UserRole",
            values=user_role_values
        )

        return APIResponse[EnumListResponse](
            success=True,
            message="User roles retrieved successfully.",
            data=response_data,
            error_code=None,
            errors=None
        )