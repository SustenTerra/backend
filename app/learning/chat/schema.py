from typing import List, Literal, Union

from pydantic import BaseModel


class Message(BaseModel):
    role: Union[Literal["user"], Literal["assistant"], Literal["system"]]
    content: str


class UpdateChat(BaseModel):
    messages: List[Message]


class ResponseChat(BaseModel):
    messages: List[Message]
