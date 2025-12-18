from backend.core.enums.field_type_enum import FieldType
from backend.application.dtos.enum_dtos import EnumValue, EnumListResponse
from backend.application.dtos.api_response import APIResponse

class GetFieldTypesUseCase:
    async def execute(self) -> APIResponse[EnumListResponse]:
        field_type_values = [EnumValue(name=member.name, value=member.value) for member in FieldType]

        response_data = EnumListResponse(
            enum_name="FieldType",
            values=field_type_values
        )

        return APIResponse[EnumListResponse](
            success=True,
            message="Field types retrieved successfully.",
            data=response_data,
            error_code=None,
            errors=None
        )