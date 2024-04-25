from sqlalchemy.orm import sessionmaker

from app.database.connection import engine
from app.service.bucket_manager import BucketManager
from app.service.openai_client import OpenAIClient
from app.service.stripe_client import StripeClient


def get_session():
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def get_openai_client():
    return OpenAIClient()


def get_bucket_manager():
    return BucketManager()


def get_stripe_client():
    return StripeClient()
