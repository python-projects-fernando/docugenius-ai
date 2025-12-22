from backend.application.file_storage.file_storage import FileStorageGateway
from backend.infrastructure.file_storage.local_file_storage import LocalFileStorageGateway


def get_local_file_storage_gateway() -> FileStorageGateway:
    return LocalFileStorageGateway(storage_directory="backend/temp_generated_docs")