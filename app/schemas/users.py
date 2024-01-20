from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(
        pattern=r"[A-z0-9_.\-]+@[A-z0-9]+\.[A-z]+(\.[A-z]+)*",
        json_schema_extra={
            "title": "Email",
            "description": "Email of the user",
            "examples": ["john.doe@gmail.com"],
        },
    )
    full_name: str = Field(
        json_schema_extra={
            "title": "Full name",
            "description": "Full name of the user",
            "examples": ["John Doe"],
        }
    )
    phone: str = Field(
        pattern=r"^[0-9]{9,15}$",
        json_schema_extra={
            "title": "Phone number",
            "description": "Phone number the user",
            "examples": ["5583999999999"],
        },
    )


class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        json_schema_extra={
            "title": "Password",
            "description": "Password of the user",
            "examples": ["John@123"],
        },
    )


class UserView(UserBase):
    id: int


class UserUpdate(BaseModel):
    email: Optional[str] = Field(
        description="Email of the user",
        default=None,
        pattern=r"[A-z0-9_.\-]+@[A-z0-9]+\.[A-z]+(\.[A-z]+)*",
    )
    full_name: Optional[str] = Field(
        description="Full name of the user", default=None
    )
    phone: Optional[str] = Field(
        description="Phone number of the user",
        default=None,
        pattern=r"^[0-9]{9,15}$",
    )

class UserUpdatePassword(BaseModel):
    current_password: str = Field(
        min_length=8,
        json_schema_extra={
            "title": "Current Password",
            "description": "Current Password of the user",
            "examples": ["John@123"],
        },
    )
    new_password: str = Field(
        min_length=8,
        alias="password",
        json_schema_extra={
            "title": "New Password",
            "description": "New Password of the user",
            "examples": ["John@321"],
        },
    )