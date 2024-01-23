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
