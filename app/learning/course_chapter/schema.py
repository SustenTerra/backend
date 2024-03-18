from datetime import datetime
from pydantic import BaseModel, Field

from app.learning.course.schema import CourseView


class CourseChapterBase(BaseModel):
    name: str = Field(
        json_schema_extra={
            "title": "name",
            "description": "One Chapter of the Course",
            "examples": ["Getting Started"],
        }
    )


class CourseChapterCreate(CourseChapterBase):
    course_id: int


class CourseChapterCreateWithIndex(CourseChapterCreate):
    index: int


class CourseChapterView(CourseChapterBase):
    name: str
    index: int
    course: CourseView
    created_at: datetime
    updated_at: datetime


class CourseChapterUpdate(CourseChapterBase):
    name: str
