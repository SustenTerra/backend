from app.schemas.users import UserView
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PostCategoryView(BaseModel):
    name: str


class PostBase(BaseModel):
    title: str
    image_url: str
    description: str
    price: float
    category_id: int


class PostCreate(PostBase):
    user_id: int = Field(default=None)


class PostUpdate(BaseModel):
    title: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None)
    category_id: Optional[int] = Field(default=None)


class PostView(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user: UserView
    category: PostCategoryView
