from app.schemas.chat import UpdateChat
from app.services.openai_client import OpenAIClient


class ChatController:
    def __init__(self, openai_client: OpenAIClient) -> None:
        self.openai_client = openai_client

    def update_chat(self, body: UpdateChat):
        return body
