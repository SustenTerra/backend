from fastapi import Depends
from sqlalchemy.orm import Session

from app.controllers.user import UserController
from app.database.connection import engine
from app.repositories.user import UserRepository


def get_session():
    session = Session(bind=engine)

    try:
        yield session
    finally:
        session.close()


def get_user_repository(session: Session = Depends(get_session)):
    return UserRepository(session)


def get_user_controller(repository: UserRepository = Depends(get_user_repository)):
    return UserController(repository)
