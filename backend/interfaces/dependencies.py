from typing import Annotated
from fastapi import Depends

from backend.application.ai_gateway.ai_gateway import AIGateway
from backend.application.repositories.document_field_repository import DocumentFieldRepository
from backend.application.repositories.document_type_repository import DocumentTypeRepository
from backend.application.repositories.user_repository import UserRepository
from backend.application.use_cases.document_field.batch_create_document_fields_use_case import \
    BatchCreateDocumentFieldsUseCase
from backend.application.use_cases.document_field.create_document_field_use_case import CreateDocumentFieldUseCase
from backend.application.use_cases.document_field.delete_document_field_use_case import DeleteDocumentFieldUseCase
from backend.application.use_cases.document_field.get_document_field_by_id_use_case import GetDocumentFieldByIdUseCase
from backend.application.use_cases.document_field.list_document_fields_by_document_type_use_case import \
    ListDocumentFieldsByDocumentTypeUseCase
from backend.application.use_cases.document_field.suggest_document_fields_use_case import SuggestDocumentFieldsUseCase
from backend.application.use_cases.document_field.update_document_field_use_case import UpdateDocumentFieldUseCase
from backend.application.use_cases.document_type.batch_create_document_types_use_case import \
    BatchCreateDocumentTypesUseCase
from backend.application.use_cases.document_type.create_document_type_use_case import CreateDocumentTypeUseCase
from backend.application.use_cases.document_type.delete_document_type_use_case import DeleteDocumentTypeUseCase
from backend.application.use_cases.document_type.get_document_type_by_id_use_case import GetDocumentTypeByIdUseCase
from backend.application.use_cases.document_type.get_document_type_by_name_use_case import GetDocumentTypeByNameUseCase
from backend.application.use_cases.document_type.list_document_types_use_case import ListDocumentTypesUseCase
from backend.application.use_cases.document_type.suggest_document_types_use_case import SuggestDocumentTypesUseCase
from backend.application.use_cases.document_type.update_document_type_use_case import UpdateDocumentTypeUseCase
from backend.application.use_cases.user.create_user_use_case import CreateUserUseCase
from backend.application.use_cases.user.delete_user_use_case import DeleteUserUseCase
from backend.application.use_cases.user.get_user_by_email_use_case import GetUserByEmailUseCase
from backend.application.use_cases.user.get_user_by_id_use_case import GetUserByIdUseCase
from backend.application.use_cases.user.get_user_by_username_use_case import GetUserByUsernameUseCase
from backend.application.use_cases.user.list_users_use_case import ListUsersUseCase
from backend.application.use_cases.user.update_user_use_case import UpdateUserUseCase
from backend.infrastructure.database.mysql_dependencies import get_mysql_document_type_repository, \
    get_mysql_user_repository, get_mysql_document_field_repository
from backend.infrastructure.gateways.hf_openai_ai_gateway import HuggingFaceOpenAIAIGateway

import os
from dotenv import load_dotenv

load_dotenv()

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


# Document Type
def get_create_document_type_use_case(
    repository: Annotated[DocumentTypeRepository, Depends(get_mysql_document_type_repository)]
) -> CreateDocumentTypeUseCase:
    return CreateDocumentTypeUseCase(repository=repository)

def get_batch_create_document_types_use_case(
    create_single_use_case: Annotated[CreateDocumentTypeUseCase, Depends(get_create_document_type_use_case)]
) -> BatchCreateDocumentTypesUseCase:
    return BatchCreateDocumentTypesUseCase(create_single_use_case=create_single_use_case)

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


# DOCUMENT FIELD
def get_create_document_field_use_case(
    document_field_repo: Annotated[DocumentFieldRepository, Depends(get_mysql_document_field_repository)],
    document_type_repo: Annotated[DocumentTypeRepository, Depends(get_mysql_document_type_repository)]
) -> CreateDocumentFieldUseCase:
    return CreateDocumentFieldUseCase(document_field_repository=document_field_repo, document_type_repository=document_type_repo)

def get_batch_create_document_fields_use_case(
    document_type_repo: Annotated[DocumentTypeRepository, Depends(get_mysql_document_type_repository)],
    document_field_repo: Annotated[DocumentFieldRepository, Depends(get_mysql_document_field_repository)]
) -> BatchCreateDocumentFieldsUseCase:
    return BatchCreateDocumentFieldsUseCase(document_type_repo=document_type_repo, document_field_repo=document_field_repo)

def get_get_document_field_by_id_use_case(
    repository: Annotated[DocumentFieldRepository, Depends(get_mysql_document_field_repository)]
) -> GetDocumentFieldByIdUseCase:
    return GetDocumentFieldByIdUseCase(repository=repository)

def get_update_document_field_use_case(
    document_field_repo: Annotated[DocumentFieldRepository, Depends(get_mysql_document_field_repository)],
    document_type_repo: Annotated[DocumentTypeRepository, Depends(get_mysql_document_type_repository)]
) -> UpdateDocumentFieldUseCase:
    return UpdateDocumentFieldUseCase(document_field_repo=document_field_repo, document_type_repo=document_type_repo)

def get_list_document_fields_by_document_type_use_case(
    document_type_repo: Annotated[DocumentTypeRepository, Depends(get_mysql_document_type_repository)],
    document_field_repo: Annotated[DocumentFieldRepository, Depends(get_mysql_document_field_repository)]
) -> ListDocumentFieldsByDocumentTypeUseCase:
    return ListDocumentFieldsByDocumentTypeUseCase(document_type_repo=document_type_repo, document_field_repo=document_field_repo)

def get_delete_document_field_use_case(
    repository: Annotated[DocumentFieldRepository, Depends(get_mysql_document_field_repository)]
) -> DeleteDocumentFieldUseCase:
    return DeleteDocumentFieldUseCase(repository=repository)

# AI
def get_hf_openai_ai_gateway() -> HuggingFaceOpenAIAIGateway:
    hf_token = os.getenv("HF_API_TOKEN")
    if not hf_token:
        raise ValueError("HF_API_TOKEN not found in environment variables.")
    base_url = os.getenv("HF_OPENAI_BASE_URL", "https://router.huggingface.co/v1")
    return HuggingFaceOpenAIAIGateway(hf_token=hf_token, base_url=base_url)

def get_suggest_document_types_use_case(
    impl: Annotated[AIGateway, Depends(get_hf_openai_ai_gateway)],
) -> SuggestDocumentTypesUseCase:
    return SuggestDocumentTypesUseCase(ai_gateway=impl)

def get_suggest_document_fields_use_case(
    impl: Annotated[AIGateway, Depends(get_hf_openai_ai_gateway)]
) -> SuggestDocumentFieldsUseCase:
    return SuggestDocumentFieldsUseCase(ai_gateway=impl)

