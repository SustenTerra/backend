from datetime import datetime
from pydantic import BaseModel, Field


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
    course_id: int
    created_at: datetime
    updated_at: datetime


class CourseChapterUpdate(CourseChapterBase):
    pass
