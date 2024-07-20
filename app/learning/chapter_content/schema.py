from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ChapterContentBase(BaseModel):
    name: str
    description: str
    video_url: str


class ChapterContentCreate(ChapterContentBase):
    course_chapter_id: int


class ChapterContentCreateWithIndex(ChapterContentBase):
    course_chapter_id: int
    index: int


class ChapterContentUpdate(BaseModel):
    name: Optional[str] = Field(
        description="Name of the content",
        default=None,
    )
    description: Optional[str] = Field(
        description="Description of the content",
        default=None,
    )
    video_url: Optional[str] = Field(
        description="URL of the content video",
        default=None,
        pattern=r"^(https?):\/\/[^\s\/$.?#].[^\s]*$",
    )


class ChapterContentView(ChapterContentBase):
    id: int
    chapter_index: int
    chapter_name: str
    course_chapter_id: int
    previous_chapter_content_id: Optional[int] = Field(default=None)
    next_chapter_content_id: Optional[int] = Field(default=None)
    created_at: datetime
    updated_at: datetime
