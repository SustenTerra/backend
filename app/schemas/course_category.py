from datetime import datetime

from pydantic import BaseModel


class CourseCategoryCreate(BaseModel):
    name: str


class CourseCategoryUpdate(BaseModel):
    name: str


class CourseCategoryView(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
