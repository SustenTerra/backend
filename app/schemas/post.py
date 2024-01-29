from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, Field

from app.schemas.users import UserView


class PostCategoryView(BaseModel):
    name: str


class PostBase(BaseModel):
    title: str
    image_url: str
    description: str
    price: int
    category_id: int


class PostCreate(PostBase):
    user_id: int


class PostCreateWithImage(BaseModel):
    title: str
    image: UploadFile
    image_url: Optional[str] = Field(default=None)
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
