from backend.application.dtos.ai_inference import InferenceRequest
from backend.application.dtos.document_type_suggestion import GenerateDocumentTypesRequest, GenerateDocumentTypesResponse, SuggestedDocumentType
from backend.application.dtos.api_response import APIResponse
from backend.application.ai_gateway.ai_gateway import AIGateway
from backend.application.prompts import GENERATE_DOCUMENT_TYPES_PROMPT
import json

class SuggestDocumentTypesUseCase:
    def __init__(self, ai_gateway: AIGateway):
        self._ai_gateway = ai_gateway

    async def execute(self, request_dto: GenerateDocumentTypesRequest) -> APIResponse[GenerateDocumentTypesResponse]:
        prompt = GENERATE_DOCUMENT_TYPES_PROMPT.format(business_description_input=request_dto.business_description)

        try:
            inference_request_dto = InferenceRequest(
                model="meta-llama/Llama-3.1-8B-Instruct:cerebras",
                prompt=prompt
            )

            ai_response = await self._ai_gateway.generate_text(inference_request_dto)

            json_str = ai_response.generated_text
            parsed_response = json.loads(json_str)
            suggested_types_raw = parsed_response.get("suggested_document_types", [])

            suggested_types_dtos = [
                SuggestedDocumentType(name=item["name"], description=item["description"])
                for item in suggested_types_raw
            ]

            response_data_dto = GenerateDocumentTypesResponse(suggested_document_types=suggested_types_dtos)

            return APIResponse[GenerateDocumentTypesResponse](
                success=True,
                message="Document types suggested successfully.",
                data=response_data_dto,
                error_code=None,
                errors=None
            )

        except json.JSONDecodeError as e:
            return APIResponse[GenerateDocumentTypesResponse](
                success=False,
                message="Failed to parse AI response for document types.",
                error_code="AI_RESPONSE_PARSE_ERROR",
                errors=[f"Invalid JSON format returned by AI: {str(e)}"],
                data=None
            )
        except KeyError as e:
            return APIResponse[GenerateDocumentTypesResponse](
                success=False,
                message="AI response is missing expected data structure.",
                error_code="AI_RESPONSE_STRUCTURE_ERROR",
                errors=[f"Missing key in AI response: {str(e)}"],
                data=None
            )
        except Exception as e:
            return APIResponse[GenerateDocumentTypesResponse](
                success=False,
                message="An unexpected error occurred during document type suggestion.",
                error_code="SUGGEST_DOC_TYPES_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )