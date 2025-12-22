from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, RedirectResponse
import os
from pathlib import Path
import mimetypes

from backend.infrastructure.database.mysql_dependencies import get_mysql_generated_document_repository
from backend.interfaces.dependencies import role_checker
from backend.core.enums.user_role_enum import UserRole
from backend.application.repositories.generated_document_repository import GeneratedDocumentRepository
from backend.core.models.user import User as CoreUser

router = APIRouter(prefix="/documents", tags=["Document Downloads - User/Admin"])

TEMP_DOCS_DIR = Path("backend") / "temp_generated_docs"

@router.get(
    "/download/{location_identifier}",
    status_code=status.HTTP_200_OK,
    summary="Download a generated document file (User/Admin)",
    description="Downloads a generated document file. For S3, generates and redirects to a presigned URL. For local, serves the file directly. Accessible by regular users and administrators. Version: v1.",
)
async def download_document(
    location_identifier: str,
    current_user: CoreUser = Depends(role_checker([UserRole.COMMON_USER, UserRole.ADMIN])),
    gen_doc_repo: GeneratedDocumentRepository = Depends(get_mysql_generated_document_repository)
):
    user_generated_docs = await gen_doc_repo.find_by_user_id(current_user.id)
    doc_record = next((doc for doc in user_generated_docs if doc.file_path_or_key == location_identifier), None)

    if not doc_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found or access denied."
        )

    storage_backend = os.getenv("STORAGE_BACKEND", "LOCAL").upper()

    if storage_backend == "S3":
        from backend.infrastructure.file_storage.s3_file_storage import S3FileStorageGateway
        s3_gateway = S3FileStorageGateway()

        try:
            presigned_url = await s3_gateway.get_file_url(location_identifier=location_identifier)
            return RedirectResponse(url=presigned_url, status_code=status.HTTP_302_FOUND)
        except Exception as e:
            print(f"Error generating S3 presigned URL: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error generating download link."
            )

    else:
        try:
            file_path = TEMP_DOCS_DIR.joinpath(location_identifier).resolve()
            file_path.relative_to(TEMP_DOCS_DIR.resolve())
        except (ValueError, RuntimeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid filename provided."
            )

        if not file_path.is_file():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found."
            )

        media_type, _ = mimetypes.guess_type(str(file_path))
        if not media_type:
            media_type = "application/octet-stream"

        return FileResponse(
            path=file_path,
            media_type=media_type,
            filename=location_identifier,
        )

# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.responses import FileResponse
# from pathlib import Path
# import mimetypes
#
# from backend.core.models.user import User
# from backend.interfaces.dependencies import role_checker
# from backend.core.enums.user_role_enum import UserRole
#
# router = APIRouter(prefix="/documents", tags=["Document Downloads - User/Admin"])
#
# TEMP_DOCS_DIR = Path("backend") / "temp_generated_docs"
#
# @router.get(
#     "/download/{filename}",
#     status_code=status.HTTP_200_OK,
#     summary="Download a generated document file (User/Admin)",
#     description="Downloads a .docx file that was previously generated based on user input and AI. Accessible by regular users and administrators. Version: v1.",
# )
# async def download_document(
#     filename: str,
#     current_user: User = Depends(role_checker([UserRole.COMMON_USER, UserRole.ADMIN]))
# ):
#     try:
#         file_path = TEMP_DOCS_DIR.joinpath(filename).resolve()
#         file_path.relative_to(TEMP_DOCS_DIR.resolve())
#     except (ValueError, RuntimeError):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid filename provided."
#         )
#
#     if not file_path.is_file():
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="File not found."
#         )
#
#     media_type, _ = mimetypes.guess_type(str(file_path))
#     if not media_type:
#         media_type = "application/octet-stream"
#
#     return FileResponse(
#         path=file_path,
#         media_type=media_type,
#         filename=filename,
#     )