from typing import Annotated, List
from fastapi import Depends,HTTPException, status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from jose import JWTError, jwt

from backend.application.ai_gateway.ai_gateway import AIGateway
from backend.application.file_storage.file_storage import FileStorageGateway
from backend.application.repositories.document_field_repository import DocumentFieldRepository
from backend.application.repositories.document_type_repository import DocumentTypeRepository
from backend.application.repositories.generated_document_repository import GeneratedDocumentRepository
from backend.application.repositories.user_repository import UserRepository
from backend.application.use_cases.auth.login_user_use_case import LoginUserUseCase
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
from backend.application.use_cases.document_type.generate_document_use_case import GenerateDocumentUseCase
from backend.application.use_cases.document_type.get_document_type_by_id_use_case import GetDocumentTypeByIdUseCase
from backend.application.use_cases.document_type.get_document_type_by_name_use_case import GetDocumentTypeByNameUseCase
from backend.application.use_cases.document_type.list_document_types_use_case import ListDocumentTypesUseCase
from backend.application.use_cases.document_type.suggest_document_types_use_case import SuggestDocumentTypesUseCase
from backend.application.use_cases.document_type.update_document_type_use_case import UpdateDocumentTypeUseCase
from backend.application.use_cases.enum.get_field_types_use_case import GetFieldTypesUseCase
from backend.application.use_cases.enum.get_user_roles_use_case import GetUserRolesUseCase
from backend.application.use_cases.user.create_user_use_case import CreateUserUseCase
from backend.application.use_cases.user.delete_user_use_case import DeleteUserUseCase
from backend.application.use_cases.user.get_user_by_email_use_case import GetUserByEmailUseCase
from backend.application.use_cases.user.get_user_by_id_use_case import GetUserByIdUseCase
from backend.application.use_cases.user.get_user_by_username_use_case import GetUserByUsernameUseCase
from backend.application.use_cases.user.list_users_use_case import ListUsersUseCase
from backend.application.use_cases.user.update_user_use_case import UpdateUserUseCase
from backend.application.use_cases.document_type.generate_document_use_case import GenerateDocumentUseCase
from backend.core.enums.user_role_enum import UserRole
from backend.infrastructure.database.mysql_dependencies import get_mysql_document_type_repository, \
    get_mysql_user_repository, get_mysql_document_field_repository, get_mysql_generated_document_repository
from backend.infrastructure.file_storage.file_storage_dependencies import get_file_storage_gateway
from backend.infrastructure.gateways.hf_openai_ai_gateway import HuggingFaceOpenAIAIGateway
from backend.core.models.user import User as CoreUser

import os
from dotenv import load_dotenv

load_dotenv()

# Auth
security_scheme = HTTPBearer(
    scheme_name="JWT",
    description="JWT authorization header using the Bearer scheme. Example: 'Bearer YOUR_JWT_ACCESS_TOKEN'",
    auto_error=True
)

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-this-in-production")
ALGORITHM = "HS256"

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    user_repo: UserRepository = Depends(get_mysql_user_repository)
) -> CoreUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")

        if user_id is None or token_type != "access":
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user_entity = await user_repo.find_by_id(int(user_id))

    if user_entity is None:
        raise credentials_exception

    if not user_entity.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user account",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_entity

def role_checker(allowed_roles: List[UserRole]):
    async def check_user_role(current_user: CoreUser = Depends(get_current_user)):
        forbidden_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Insufficient privileges.",
            headers={"WWW-Authenticate": "Bearer"},
        )

        if current_user.role not in allowed_roles:
            raise forbidden_exception

        return current_user
    return check_user_role

def get_login_user_use_case(
    user_repo: Annotated[UserRepository, Depends(get_mysql_user_repository)]
) -> LoginUserUseCase:
    return LoginUserUseCase(user_repository=user_repo)


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

def get_get_user_roles_use_case() -> GetUserRolesUseCase:
    return GetUserRolesUseCase()


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

def get_get_field_types_use_case() -> GetFieldTypesUseCase:
    return GetFieldTypesUseCase()

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



def get_generate_document_use_case(
    doc_type_repo: Annotated[DocumentTypeRepository, Depends(get_mysql_document_type_repository)],
    doc_field_repo: Annotated[DocumentFieldRepository, Depends(get_mysql_document_field_repository)],
    gen_doc_repo: Annotated[GeneratedDocumentRepository, Depends(get_mysql_generated_document_repository)],
    ai_gw: Annotated[AIGateway, Depends(get_hf_openai_ai_gateway)],
    file_storage_gw: Annotated[FileStorageGateway, Depends(get_file_storage_gateway)]
) -> GenerateDocumentUseCase:
    return GenerateDocumentUseCase(
        document_type_repo=doc_type_repo,
        document_field_repo=doc_field_repo,
        generated_document_repo=gen_doc_repo,
        ai_gateway=ai_gw,
        file_storage_gateway=file_storage_gw
    )