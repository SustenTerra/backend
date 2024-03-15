from sqlalchemy.orm import sessionmaker

from app.database.connection import engine
from app.service.openai_client import OpenAIClient


def get_session():
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def get_openai_client():
    return OpenAIClient()
