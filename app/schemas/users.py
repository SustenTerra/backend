from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(description="Email of the user")
    full_name: str = Field(description="Full name of the user")


class UserCreate(UserBase):
    password: str = Field(description="Password of the user")


class UserView(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[str] = Field(description="Email of the user", default=None)
    full_name: Optional[str] = Field(description="Full name of the user", default=None)
    password: Optional[str] = Field(description="Password of the user", default=None)
