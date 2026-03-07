# backend/application/use_cases/document_type/get_document_types_with_fields_use_case.py
from typing import List as TypingList # Importa como TypingList para evitar confusão com built-in list
import math # Importa math para calcular o número de páginas
from backend.application.repositories.document_type_repository import DocumentTypeRepository
from backend.core.models.document_type import DocumentType
from backend.application.dtos.document_type import DocumentTypeResponse, DocumentTypeListResponse
from backend.application.dtos.pagination_params import PaginationParams # Importa o DTO de paginação
from backend.application.dtos.api_response import APIResponse

class GetDocumentTypesWithFieldsUseCase:
    def __init__(self, repository: DocumentTypeRepository):
        self._repository = repository

    # Agora o metodo execute recebe os parametros de paginação
    async def execute(self, pagination: PaginationParams) -> APIResponse[DocumentTypeListResponse]:
        try:
            # 1. Calcula o offset para paginação
            offset = (pagination.page - 1) * pagination.size

            # 2. Chama o repositório para buscar os tipos com campos, de forma paginada
            # Isso exigirá que você também atualize o repositório e sua implementação
            items_core = await self._repository.find_with_fields_paginated(offset=offset, limit=pagination.size)

            # 3. Calcula o total de tipos com campos
            # Isso exigirá um novo método no repositório também
            total = await self._repository.count_with_fields()

            # 4. Calcula o número total de páginas
            total_pages = math.ceil(total / pagination.size) if total > 0 else 0

            # 5. Mape para DTOs de resposta
            items_response_dto = [
                DocumentTypeResponse(
                    id=entity.id,
                    name=entity.name,
                    description=entity.description
                )
                for entity in items_core
            ]

            # 6. Prepara o DTO de resposta da lista paginada
            list_response_dto = DocumentTypeListResponse(
                items=items_response_dto,
                total=total,
                page=pagination.page,
                size=pagination.size,
                pages=total_pages
            )

            # 7. Retorna uma resposta de sucesso com o DTO de lista
            return APIResponse[DocumentTypeListResponse](
                success=True,
                message="Document types with associated fields retrieved successfully.",
                data=list_response_dto,
                error_code=None,
                errors=None
            )

        except Exception as e:
            # 8. Retorna uma resposta de erro em caso de exceção
            return APIResponse[DocumentTypeListResponse](
                success=False,
                message="An unexpected error occurred while retrieving document types with fields.",
                error_code="GET_DT_WITH_FIELDS_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )