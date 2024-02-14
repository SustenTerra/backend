from fastapi import APIRouter, Depends

from app.controllers.chat import ChatController
from app.deps import get_chat_controller
from app.schemas.chat import ResponseChat, UpdateChat
from app.services.auth import get_logged_user

chat = APIRouter(tags=["chat"], dependencies=[Depends(get_logged_user)])


@chat.post("/chat", response_model=ResponseChat)
def update_chat(
    body: UpdateChat,
    chat_controller: ChatController = Depends(get_chat_controller),
):
    return chat_controller.update_chat(body)
