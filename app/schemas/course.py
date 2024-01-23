from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    name: str
    description: str
    author_name: str


class CourseUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    author_name: Optional[str] = Field(default=None)


class CourseListView(BaseModel):
    id: int
    name: str
    author_name: str
    category_name: str
    chapters_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
