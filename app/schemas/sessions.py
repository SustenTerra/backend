from pydantic import BaseModel, Field

from app.schemas.users import UserView


class LoginPayload(BaseModel):
    email: str = Field(
        pattern=r"[A-z0-9_.\-]+@[A-z0-9]+\.[A-z]+(\.[A-z]+)*",
        json_schema_extra={
            "title": "Email",
            "description": "Email of the user",
            "examples": ["john.doe@gmail.com"],
        },
    )
    password: str


class LoginView(BaseModel):
    token: str
    user: UserView
