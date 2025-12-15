from typing import Annotated
from fastapi import Depends

from backend.application.repositories.document_type_repository import DocumentTypeRepository
from backend.application.repositories.user_repository import UserRepository
from backend.application.use_cases.document_type.create_document_type_use_case import CreateDocumentTypeUseCase
from backend.application.use_cases.document_type.delete_document_type_use_case import DeleteDocumentTypeUseCase
from backend.application.use_cases.document_type.get_document_type_by_id_use_case import GetDocumentTypeByIdUseCase
from backend.application.use_cases.document_type.get_document_type_by_name_use_case import GetDocumentTypeByNameUseCase
from backend.application.use_cases.document_type.list_document_types_use_case import ListDocumentTypesUseCase
from backend.application.use_cases.document_type.update_document_type_use_case import UpdateDocumentTypeUseCase
from backend.application.use_cases.user.create_user_use_case import CreateUserUseCase
from backend.infrastructure.database.mysql_dependencies import get_mysql_document_type_repository, \
    get_mysql_user_repository


# Document Type
def get_create_document_type_use_case(
    repository: Annotated[DocumentTypeRepository, Depends(get_mysql_document_type_repository)]
) -> CreateDocumentTypeUseCase:
    return CreateDocumentTypeUseCase(repository=repository)

def get_update_document_type_use_case(
    repository: Annotated[DocumentTypeRepository, Depends(get_mysql_document_type_repository)]
) -> UpdateDocumentTypeUseCase:
    return UpdateDocumentTypeUseCase(repository=repository)

def get_delete_document_type_use_case(
    repository: Annotated[DocumentTypeRepository, Depends(get_mysql_document_type_repository)]
) -> DeleteDocumentTypeUseCase:
    return DeleteDocumentTypeUseCase(repository=repository)

def get_list_document_types_use_case(
    repository: Annotated[DocumentTypeRepository, Depends(get_mysql_document_type_repository)]
) -> ListDocumentTypesUseCase:
    return ListDocumentTypesUseCase(repository=repository)

def get_get_document_type_by_id_use_case(
    repository: Annotated[DocumentTypeRepository, Depends(get_mysql_document_type_repository)]
) -> GetDocumentTypeByIdUseCase:
    return GetDocumentTypeByIdUseCase(repository=repository)

def get_get_document_type_by_name_use_case(
    repository: Annotated[DocumentTypeRepository, Depends(get_mysql_document_type_repository)]
) -> GetDocumentTypeByNameUseCase:
    return GetDocumentTypeByNameUseCase(repository=repository)


# User
def get_create_user_use_case(
    repository: Annotated[UserRepository, Depends(get_mysql_user_repository)]
) -> CreateUserUseCase:
    return CreateUserUseCase(repository=repository)