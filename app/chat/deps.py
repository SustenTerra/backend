from fastapi import Depends

from app.chat.controller import ChatController
from app.deps import get_openai_client
from app.service.openai_client import OpenAIClient


def get_chat_controller(
    openai_client: OpenAIClient = Depends(get_openai_client),
):
    return ChatController(openai_client)
