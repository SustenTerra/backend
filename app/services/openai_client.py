from fastapi import HTTPException
from openai import AuthenticationError, OpenAI

from app.config import Config
from app.schemas.chat import UpdateChat


class OpenAIClient:
    def __init__(self) -> None:
        self.config = Config()
        self.client = OpenAI(api_key=self.config.OPEN_AI_KEY)

    def get_new_message(self, chat: UpdateChat):
        try:
            response = self.client.chat.completions.create(
                model=self.config.MODEL_NAME,
                messages=chat.model_dump()["messages"],
                temperature=self.config.MODEL_TEMPERATURE,
            )
            return response.choices[0].message.content
        except AuthenticationError:
            raise HTTPException(
                status_code=401,
                detail="Invalid OpenAI key",
            )
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Something went wrong with the OpenAI API",
            )
