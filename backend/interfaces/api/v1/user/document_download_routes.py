from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pathlib import Path
import mimetypes

from backend.core.models.user import User
from backend.interfaces.dependencies import role_checker
from backend.core.enums.user_role_enum import UserRole

router = APIRouter(prefix="/documents", tags=["Document Downloads - User/Admin"])

TEMP_DOCS_DIR = Path("backend") / "temp_generated_docs"

@router.get(
    "/download/{filename}",
    status_code=status.HTTP_200_OK,
    summary="Download a generated document file (User/Admin)",
    description="Downloads a .docx file that was previously generated based on user input and AI. Accessible by regular users and administrators. Version: v1.",
)
async def download_document(
    filename: str,
    current_user: User = Depends(role_checker([UserRole.COMMON_USER, UserRole.ADMIN]))
):
    try:
        file_path = TEMP_DOCS_DIR.joinpath(filename).resolve()
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
        filename=filename,
    )