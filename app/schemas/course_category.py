from pydantic import BaseModel


class CourseCategoryCreate(BaseModel):
    name: str


class CourseCategoryUpdate(BaseModel):
    name: str
