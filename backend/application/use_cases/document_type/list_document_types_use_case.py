from typing import List as TypingList
import math
from backend.application.repositories.document_type_repository import DocumentTypeRepository
from backend.application.dtos.document_type import DocumentTypeResponse, DocumentTypeListResponse, PaginationParams
from backend.application.dtos.api_response import APIResponse

class ListDocumentTypesUseCase:
    def __init__(self, repository: DocumentTypeRepository):
        self._repository = repository

    async def execute(self, pagination: PaginationParams) -> APIResponse[DocumentTypeListResponse]:
        try:
            offset = (pagination.page - 1) * pagination.size
            items_core = await self._repository.find_all_paginated(offset=offset, limit=pagination.size)
            total = await self._repository.count_all()
            total_pages = math.ceil(total / pagination.size) if total > 0 else 0

            items_response_dto = [
                DocumentTypeResponse(
                    id=entity.id,
                    name=entity.name,
                    description=entity.description
                )
                for entity in items_core
            ]

            list_response_dto = DocumentTypeListResponse(
                items=items_response_dto,
                total=total,
                page=pagination.page,
                size=pagination.size,
                pages=total_pages
            )

            return APIResponse[DocumentTypeListResponse](
                success=True,
                message="Document types retrieved successfully.",
                data=list_response_dto,
                error_code=None,
                errors=None
            )

        except Exception as e:
            return APIResponse[DocumentTypeListResponse](
                success=False,
                message="An unexpected error occurred while retrieving document types.",
                error_code="LIST_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )