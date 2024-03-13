from fastapi import APIRouter, Depends

from app.chat.controller import ChatController
from app.deps import get_chat_controller
from app.models import User
from app.chat.schema import ResponseChat, UpdateChat
from app.service.auth import get_logged_user

chat = APIRouter(tags=["chat"])


@chat.post("/chat", response_model=ResponseChat)
def update_chat(
    body: UpdateChat,
    chat_controller: ChatController = Depends(get_chat_controller),
    user: User = Depends(get_logged_user),
):
    return chat_controller.update_chat(body, user)