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
from backend.application.use_cases.user.delete_user_use_case import DeleteUserUseCase
from backend.application.use_cases.user.get_user_by_email_use_case import GetUserByEmailUseCase
from backend.application.use_cases.user.get_user_by_id_use_case import GetUserByIdUseCase
from backend.application.use_cases.user.get_user_by_username_use_case import GetUserByUsernameUseCase
from backend.application.use_cases.user.list_users_use_case import ListUsersUseCase
from backend.application.use_cases.user.update_user_use_case import UpdateUserUseCase
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

def get_update_user_use_case(
    repository: Annotated[UserRepository, Depends(get_mysql_user_repository)]
) -> UpdateUserUseCase:
    return UpdateUserUseCase(repository=repository)

def get_delete_user_use_case(
    repository: Annotated[UserRepository, Depends(get_mysql_user_repository)]
) -> DeleteUserUseCase:
    return DeleteUserUseCase(repository=repository)

def get_get_user_by_id_use_case(
    repository: Annotated[UserRepository, Depends(get_mysql_user_repository)]
) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(repository=repository)

def get_get_user_by_username_use_case(
    repository: Annotated[UserRepository, Depends(get_mysql_user_repository)]
) -> GetUserByUsernameUseCase:
    return GetUserByUsernameUseCase(repository=repository)

def get_get_user_by_email_use_case(
    repository: Annotated[UserRepository, Depends(get_mysql_user_repository)]
) -> GetUserByEmailUseCase:
    return GetUserByEmailUseCase(repository=repository)

def get_list_users_use_case(
    repository: Annotated[UserRepository, Depends(get_mysql_user_repository)]
) -> ListUsersUseCase:
    return ListUsersUseCase(repository=repository)