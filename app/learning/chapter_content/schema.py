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
    index: int


class ChapterContentUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    video_url: Optional[str] = Field(default=None)


class ChapterContentView(ChapterContentBase):
    id: int
    chapter_index: int
    chapter_name: str
    previous_chapter_content_id: Optional[int] = Field(default=None)
    next_chapter_content_id: Optional[int] = Field(default=None)
    created_at: datetime
    updated_at: datetime
