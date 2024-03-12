from app.models import User
from app.chat.schema import Message, ResponseChat, UpdateChat
from app.service.openai_client import OpenAIClient
from app.service.prompts import get_system_prompts


class ChatController:
    def __init__(self, openai_client: OpenAIClient) -> None:
        self.openai_client = openai_client

    def update_chat(self, body: UpdateChat, user: User):
        messages = get_system_prompts(user_name=user.full_name)
        messages.extend(body.messages)

        new_content = self.openai_client.get_new_message(
            UpdateChat(messages=messages)
        )
        if not new_content:
            return ResponseChat(messages=messages)

        new_message = Message(
            role="assistant",
            content=new_content,
        )

        return ResponseChat(messages=body.messages + [new_message])
