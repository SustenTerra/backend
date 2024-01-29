import time

import boto3
from fastapi import UploadFile

from app.config import Config


class BucketManager:
    def __init__(self) -> None:
        self.config = Config()

        self.client = boto3.client(
            "s3",
            aws_access_key_id=self.config.AWS_ACCESS_KEY,
            aws_secret_access_key=self.config.AWS_ACCESS_KEY_SECRET,
            region_name=self.config.AWS_REGION,
        )

        self.bucket_name = self.config.AWS_BUCKET_NAME

    def upload_file(self, file: UploadFile):
        timestamp = int(time.time())
        object_key = f"{timestamp}-{file.filename}"

        self.client.upload_fileobj(file.file, self.bucket_name, object_key)
        return object_key

    def get_presigned_url(self, object_key: str) -> str:
        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket_name, "Key": object_key},
            ExpiresIn=self.config.AWS_BUCKET_EXPIRATION,
        )
