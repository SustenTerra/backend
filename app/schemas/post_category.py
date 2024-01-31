from datetime import datetime

from pydantic import BaseModel


class PostCategoryCreate(BaseModel):
    name: str


class PostCategoryUpdate(BaseModel):
    name: str


class PostCategoryView(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
