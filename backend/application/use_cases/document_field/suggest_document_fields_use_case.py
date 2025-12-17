from backend.application.dtos.ai_inference import InferenceRequest
from backend.application.dtos.document_field_suggestion import GenerateDocumentFieldsRequest, GenerateDocumentFieldsResponse, SuggestedDocumentField
from backend.application.dtos.api_response import APIResponse
from backend.application.ai_gateway.ai_gateway import AIGateway
from backend.application.prompts import GENERATE_DOCUMENT_FIELDS_PROMPT
import json

class SuggestDocumentFieldsUseCase:
    def __init__(self, ai_gateway: AIGateway):
        self._ai_gateway = ai_gateway

    async def execute(self, request_dto: GenerateDocumentFieldsRequest) -> APIResponse[GenerateDocumentFieldsResponse]:
        prompt = GENERATE_DOCUMENT_FIELDS_PROMPT.format(
            document_type_name=request_dto.document_type_name,
            document_type_description=request_dto.document_type_description
        )

        try:
            inference_request_dto = InferenceRequest(
                model="meta-llama/Llama-3.1-8B-Instruct:cerebras",
                prompt=prompt
            )

            ai_response = await self._ai_gateway.generate_text(inference_request_dto)
            json_str = ai_response.generated_text

            try:
                parsed_response = json.loads(json_str)
            except json.JSONDecodeError as e:
                return APIResponse[GenerateDocumentFieldsResponse](
                    success=False,
                    message="Failed to parse AI response for document fields.",
                    error_code="AI_RESPONSE_PARSE_ERROR",
                    errors=[f"Invalid JSON format returned by AI: {str(e)}"],
                    data=None
                )

            suggested_fields_raw = parsed_response.get("fields", [])
            if not isinstance(suggested_fields_raw, list):
                 return APIResponse[GenerateDocumentFieldsResponse](
                     success=False,
                     message="AI response format is invalid: 'fields' is not a list.",
                     error_code="AI_RESPONSE_FORMAT_ERROR",
                     errors=["AI response 'fields' attribute is not an array."],
                     data=None
                 )

            suggested_fields_dtos = []
            for item in suggested_fields_raw:
                name = item.get("name")
                field_type = item.get("type")
                is_required = item.get("required", False)
                description = item.get("description", "")

                if not name or not field_type:
                    continue

                field_dto = SuggestedDocumentField(
                    name=name,
                    type=field_type,
                    required=is_required,
                    description=description
                )
                suggested_fields_dtos.append(field_dto)

            response_data_dto = GenerateDocumentFieldsResponse(
                document_type=parsed_response.get("document_type", request_dto.document_type_name),
                description=parsed_response.get("description", request_dto.document_type_description),
                fields=suggested_fields_dtos
            )

            return APIResponse[GenerateDocumentFieldsResponse](
                success=True,
                message="Document fields suggested successfully.",
                data=response_data_dto,
                error_code=None,
                errors=None
            )

        except KeyError as e:
            return APIResponse[GenerateDocumentFieldsResponse](
                success=False,
                message="AI response is missing expected data structure for fields.",
                error_code="AI_RESPONSE_STRUCTURE_ERROR",
                errors=[f"Missing key in AI response: {str(e)}"],
                data=None
            )
        except Exception as e:
            return APIResponse[GenerateDocumentFieldsResponse](
                success=False,
                message="An unexpected error occurred during document field suggestion.",
                error_code="SUGGEST_DOC_FIELDS_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )