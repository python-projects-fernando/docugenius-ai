from typing import List
from backend.application.repositories.document_field_repository import DocumentFieldRepository
from backend.application.repositories.document_type_repository import DocumentTypeRepository
from backend.core.models.document_type import DocumentType as CoreDocumentType
from backend.core.models.document_field import DocumentField as CoreDocumentField
from backend.application.dtos.document_field import DocumentFieldResponse, DocumentFieldListResponse
from backend.application.dtos.api_response import APIResponse

class ListDocumentFieldsByDocumentTypeUseCase:
    def __init__(self, document_type_repo: DocumentTypeRepository, document_field_repo: DocumentFieldRepository):
        self._document_type_repo = document_type_repo
        self._document_field_repo = document_field_repo

    async def execute(self, document_type_id: int) -> APIResponse[DocumentFieldListResponse]:
        try:
            parent_doc_type: CoreDocumentType = await self._document_type_repo.find_by_id(document_type_id)
            if not parent_doc_type:
                return APIResponse[DocumentFieldListResponse](
                    success=False,
                    message=f"Parent DocumentType with ID {document_type_id} not found.",
                    error_code="PARENT_DOC_TYPE_NOT_FOUND",
                    errors=[f"Cannot list fields: Parent DocumentType with ID {document_type_id} does not exist."],
                    data=None
                )

            fields_core_entities: List[CoreDocumentField] = await self._document_field_repo.find_all_by_document_type(document_type_id)

            fields_response_dtos = [
                DocumentFieldResponse(
                    id=entity.id,
                    document_type_id=entity.document_type_id,
                    name=entity.name,
                    field_type=entity.field_type,
                    is_required=entity.is_required,
                    description=entity.description
                )
                for entity in fields_core_entities
            ]

            response_data_dto = DocumentFieldListResponse(items=fields_response_dtos)

            return APIResponse[DocumentFieldListResponse](
                success=True,
                message=f"Successfully retrieved {len(fields_response_dtos)} fields for DocumentType ID {document_type_id}.",
                data=response_data_dto,
                error_code=None,
                errors=None
            )

        except Exception as e:
            return APIResponse[DocumentFieldListResponse](
                success=False,
                message="An unexpected error occurred during document field listing.",
                error_code="LIST_FIELDS_ERROR",
                errors=[f"Internal error: {str(e)}"],
                data=None
            )