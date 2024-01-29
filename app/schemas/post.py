from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, Field, computed_field

from app.schemas.users import UserView
from app.services.bucket_manager import BucketManager


class PostCategoryView(BaseModel):
    name: str


class PostBase(BaseModel):
    title: str
    image_key: str
    description: str
    price: int
    category_id: int


class PostCreate(PostBase):
    user_id: int


class PostCreateWithImage(BaseModel):
    title: str
    image: UploadFile
    description: str
    price: int
    category_id: int
    user_id: int


class PostUpdate(BaseModel):
    title: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    price: Optional[int] = Field(default=None)
    category_id: Optional[int] = Field(default=None)


class PostView(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user: UserView
    category: PostCategoryView

    @computed_field
    @property
    def image_url(self) -> str:
        bucket_manager = BucketManager()
        return bucket_manager.get_presigned_url(self.image_key)


CREATE_POST_OPENAPI_SCHEMA = {
    "requestBody": {
        "content": {
            "multipart/form-data": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "isRequired": True},
                        "image": {
                            "type": "string",
                            "format": "binary",
                            "required": True,
                        },
                        "description": {
                            "type": "string",
                            "required": True,
                        },
                        "price": {"type": "integer", "required": True},
                        "category_id": {
                            "type": "integer",
                            "required": True,
                        },
                    },
                },
            },
        },
    },
}
