import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Config(BaseModel):
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5433")
    DB_NAME: str = os.getenv("DB_NAME", "mydatabase")
    DB_USER: str = os.getenv("DB_USER", "myuser")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "mypassword")
