from fastapi import APIRouter, Depends

from app.schemas.chat import UpdateChat
from app.services.auth import get_logged_user

chat = APIRouter(tags=["chat"], dependencies=[Depends(get_logged_user)])


@chat.post("/chat")
def update_chat(body: UpdateChat):
    return body
