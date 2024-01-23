from typing import Optional

from pydantic import BaseModel, Field


class ChapterContentCreate(BaseModel):
    name: str
    index: int
    description: str
    video_url: str


class ChapterContentUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    index: Optional[int] = Field(default=None)
    description: Optional[str] = Field(default=None)
    video_url: Optional[str] = Field(default=None)
