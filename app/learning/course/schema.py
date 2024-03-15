from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.learning.course_category.schema import CourseCategoryView


class CourseBase(BaseModel):
    name: str = Field(
        json_schema_extra={
            "title": "name",
            "description": "Name of the course",
            "examples": ["Geotinta Course"],
        }
    )
    author_name: str = Field(
        json_schema_extra={
            "title": "author_name",
            "description": "Name of the course author",
            "examples": ["Jhon Doe"],
        }
    )

    image_url: str = Field(
        json_schema_extra={
            "title": "image_url",
            "description": "Url of the image",
            "examples": ["pinterest.com"],
        }
    )
    description: str = Field(
        json_schema_extra={
            "title": "description",
            "description": "Description of the course",
            "examples": ["it's about how to extract geotinta"],
        }
    )
    course_category_id: int = Field(
        json_schema_extra={
            "title": "course_category_id",
            "description": "Id of the category of the course",
            "examples": ["1"],
        }
    )


class CourseCreate(CourseBase):
    pass


class CourseCreateWithAuthorId(CourseBase):
    author_id: int


class CourseUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    author_name: Optional[str] = Field(default=None)


class CourseListView(BaseModel):
    id: int
    name: str
    image_url: str
    author_name: str
    category_name: str
    chapters_count: int
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
    image_url: str
    author_name: str
    description: str
    created_at: datetime
    updated_at: datetime
    course_chapters: List[CourseChapterView]
    course_category: CourseCategoryView
