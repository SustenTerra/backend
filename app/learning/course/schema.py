from datetime import datetime
from typing import List, Optional

from fastapi import UploadFile
from fastapi.logger import logger
from pydantic import BaseModel, Field, computed_field

from app.learning.course_category.schema import CourseCategoryView
from app.service.bucket_manager import BucketManager


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
    image_key: str
    author_id: int


class CourseCreateWithImage(CourseBase):
    image: UploadFile


class CourseUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    author_name: Optional[str] = Field(default=None)


class CourseWithImageUrl(BaseModel):
    id: int
    image_key: str

    @computed_field
    @property
    def image_url(self) -> Optional[str]:
        bucket_manager = BucketManager()

        try:
            return bucket_manager.get_presigned_url(self.image_key)
        except Exception as error:
            logger.error(
                ("Error while getting presigned url " f"for course {self.id}: {error}")
            )
            return None


class CourseListView(CourseWithImageUrl):
    name: str
    author_name: str
    author_id: Optional[int] = Field(default=None)
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


class CourseView(CourseWithImageUrl):
    name: str
    author_name: str
    description: str
    created_at: datetime
    updated_at: datetime
    course_chapters: List[CourseChapterView]
    course_category: CourseCategoryView


class CoursePublishedUpdate(BaseModel):
    published_at: datetime
