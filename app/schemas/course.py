from datetime import datetime
from typing import List, Optional

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


class CourseCategoryView(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class CourseChapterContentView(BaseModel):
    id: int
    name: str
    index: int
    description: str
    video_url: Optional[str] = Field(default=None)
    was_viewed: Optional[bool] = Field(default=False)
    is_available: Optional[bool] = Field(default=False)
    created_at: datetime
    updated_at: datetime


class CourseChapterView(BaseModel):
    id: int
    name: str
    index: int
    course_id: int
    chapter_contents: List[CourseChapterContentView]
    created_at: datetime
    updated_at: datetime


class CourseView(BaseModel):
    id: int
    name: str
    author_name: str
    description: str
    created_at: datetime
    updated_at: datetime
    course_chapters: List[CourseChapterView]
    course_category: CourseCategoryView
