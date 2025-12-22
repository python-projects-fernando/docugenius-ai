from backend.application.file_storage.file_storage import FileStorageGateway
from backend.infrastructure.file_storage.local_file_storage import LocalFileStorageGateway
import os
from backend.infrastructure.file_storage.s3_file_storage import S3FileStorageGateway


def get_file_storage_gateway() -> FileStorageGateway:

    storage_backend = os.getenv("STORAGE_BACKEND", "LOCAL")

    if storage_backend.upper() == "S3":
        print("Using S3 File Storage Gateway")
        return S3FileStorageGateway()
    else:
        print("Using Local File Storage Gateway")
        return LocalFileStorageGateway(storage_directory="backend/temp_generated_docs")