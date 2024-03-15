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
    index: int = Field(
        json_schema_extra={
            "title": "index",
            "description": "Index of the Chapter",
            "examples": ["1"],
        }
    )


class CourseChapterCreate(CourseChapterBase):
    pass


class CourseChapterCreateWithCoursId(CourseChapterBase):
    course_id: int


class CourseChapterView(CourseChapterBase):
    id: int
    name: str
    index: int
    course: CourseView
    created_at: datetime
    updated_at: datetime
