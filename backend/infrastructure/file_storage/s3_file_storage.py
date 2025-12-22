import os
import asyncio
import boto3
from botocore.exceptions import ClientError
from backend.application.file_storage.file_storage import FileStorageGateway

class S3FileStorageGateway(FileStorageGateway):
    def __init__(self):
        self._bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
        self._region_name = os.getenv("AWS_S3_REGION")

        if not self._bucket_name or not self._region_name:
            raise ValueError("AWS_S3_BUCKET_NAME and AWS_S3_REGION must be set in environment variables.")

        self._s3_client = boto3.client(
            's3',
            region_name=self._region_name
        )

    async def save_document(self, content: bytes, filename: str) -> str:
        try:
            s3_key = filename

            def _upload_to_s3():
                self._s3_client.put_object(
                    Bucket=self._bucket_name,
                    Key=s3_key,
                    Body=content,
                )

            await asyncio.to_thread(_upload_to_s3)
            return s3_key

        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"Error uploading file to S3: {error_code} - {error_message}")
            raise

    async def get_file_url(self, location_identifier: str) -> str:
        try:
            params = {
                'Bucket': self._bucket_name,
                'Key': location_identifier,
            }

            expiration_time = 3600

            def _generate_presigned_url():
                return self._s3_client.generate_presigned_url(
                    'get_object',
                    Params=params,
                    ExpiresIn=expiration_time
                )

            presigned_url = await asyncio.to_thread(_generate_presigned_url)
            return presigned_url

        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"Error generating presigned URL from S3: {error_code} - {error_message}")
            raise