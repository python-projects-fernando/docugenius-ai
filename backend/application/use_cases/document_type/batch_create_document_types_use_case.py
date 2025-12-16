from backend.application.repositories.document_type_repository import DocumentTypeRepository
from backend.application.use_cases.document_type.create_document_type_use_case import CreateDocumentTypeUseCase
from backend.application.dtos.document_type import CreateDocumentTypeRequest, DocumentTypeResponse
from backend.application.dtos.api_response import APIResponse
from typing import List

class BatchCreateDocumentTypesUseCase:
    def __init__(self, create_single_use_case: CreateDocumentTypeUseCase):
        self._create_single_use_case = create_single_use_case

    async def execute(self, request_dtos: List[CreateDocumentTypeRequest]) -> APIResponse[List[DocumentTypeResponse]]:
        results = []
        errors_occurred = False
        error_messages = []

        for request_dto in request_dtos:
            single_result = await self._create_single_use_case.execute(request_dto)

            if single_result.success:
                results.append(single_result.data)
            else:
                errors_occurred = True
                error_messages.extend(single_result.errors or [f"Unknown error for item with name '{request_dto.name}'"])

        if errors_occurred:
            return APIResponse[List[DocumentTypeResponse]](
                success=False,
                message="Some document types failed to be created during batch operation.",
                error_code="BATCH_CREATE_PARTIAL_ERROR",
                errors=error_messages,
                data=results
            )

        return APIResponse[List[DocumentTypeResponse]](
            success=True,
            message="All document types created successfully in batch.",
            data=results,
            error_code=None,
            errors=None
        )