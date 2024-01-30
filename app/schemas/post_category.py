from pydantic import BaseModel


class PostCategoryCreate(BaseModel):
    name: str


class PostCategoryUpdate(BaseModel):
    name: str
