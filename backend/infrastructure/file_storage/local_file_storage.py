import asyncio
from pathlib import Path
from backend.application.file_storage.file_storage import FileStorageGateway

class LocalFileStorageGateway(FileStorageGateway):
    def __init__(self, storage_directory: str = "backend/temp_generated_docs"):
        self._storage_dir = Path(storage_directory)
        self._storage_dir.mkdir(parents=True, exist_ok=True)

    async def save_document(self, content: bytes, filename: str) -> str:
        file_path = self._storage_dir / filename

        try:
            file_path.resolve().relative_to(self._storage_dir.resolve())
        except (ValueError, RuntimeError):
             raise ValueError(f"Invalid filename provided: {filename}. Path traversal detected.")

        def _write_file():
            with open(file_path, 'wb') as f:
                f.write(content)

        await asyncio.to_thread(_write_file)

        return filename

    async def get_file_url(self, location_identifier: str) -> str:
        return f"/api/v1/user/documents/download/{location_identifier}"