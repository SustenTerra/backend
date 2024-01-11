from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker

from app.controllers.user import UserController
from app.database.connection import engine
from app.models import User
from app.repositories.user import UserRepository


def get_session():
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def get_user_repository(session: Session = Depends(get_session)):
    return UserRepository(User, session)


def get_user_controller(
    repository: UserRepository = Depends(get_user_repository),
):
    return UserController(User, repository)
