import random
import time

import boto3

from app.config import Config


class BucketManager:
    def __init__(self) -> None:
        config = Config()

        self.client = boto3.client(
            "s3",
            aws_access_key_id=config.AWS_ACCESS_KEY,
            aws_secret_access_key=config.AWS_ACCESS_KEY_SECRET,
            region_name=config.AWS_REGION,
        )

        self.bucket_name = config.AWS_BUCKET_NAME

    def upload_file(self, file):
        int_part = random.randint(0, 100000)
        timestamp = int(time.time())
        object_key = f"{timestamp}-{int_part}"

        self.client.upload_file(
            file,
            self.bucket_name,
            Key=object_key,
        )
        return object_key

    def get_presigned_url(self, object_key: str):
        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket_name, "Key": object_key},
            ExpiresIn=3600,
        )
