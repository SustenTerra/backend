from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    email: str = Field(description="Email of the user")
    password: str = Field(description="Password of the user")
    full_name: str = Field(description="Full name of the user")
