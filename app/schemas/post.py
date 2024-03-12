from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import UploadFile
from fastapi.logger import logger
from pydantic import BaseModel, Field, computed_field

from app.post_category.schema import PostCategoryView
from app.users.schema import UserView
from app.services.bucket_manager import BucketManager


class PostTypeEnum(Enum):
    ad = "ad"
    event = "event"
    any_service = "any_service"
    art_service = "art_service"


class PostBase(BaseModel):
    title: str
    description: str
    post_type: str
    location: str
    price: Optional[int]
    category_id: int
    user_id: int


class PostCreate(PostBase):
    image_key: str


class PostCreateWithImage(PostBase):
    image: UploadFile


class PostUpdateBase(BaseModel):
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    post_type: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)
    price: Optional[int] = Field(default=None)
    views: Optional[int] = Field(default=None)
    category_id: Optional[int] = Field(default=None)


class PostUpdate(PostUpdateBase):
    image_key: Optional[str] = Field(default=None)


class PostUpdateWithImage(PostUpdateBase):
    image: Optional[UploadFile] = Field(default=None)


class PostView(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    image_key: str
    views: int
    user: UserView
    category: PostCategoryView

    @computed_field
    @property
    def image_url(self) -> Optional[str]:
        bucket_manager = BucketManager()

        try:
            return bucket_manager.get_presigned_url(self.image_key)
        except Exception as error:
            logger.error(
                (
                    "Error while getting presigned url "
                    f"for post {self.id}: {error}"
                )
            )
            return None
