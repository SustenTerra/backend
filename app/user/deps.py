from fastapi import Depends
from sqlalchemy.orm import Session

from app.deps import get_session
from app.models import User, UserContentStatus
from app.session.controller import SessionController
from app.user.content_status import UserContentStatusRepository
from app.user.controller import UserController
from app.user.repository import UserRepository


def get_user_repository(session: Session = Depends(get_session)):
    return UserRepository(User, session)


def get_user_content_status_repository(
    session: Session = Depends(get_session),
):
    return UserContentStatusRepository(UserContentStatus, session)


def get_user_controller(
    repository: UserRepository = Depends(get_user_repository),
):
    return UserController(User, repository)


def get_session_controller(
    user_repository: UserRepository = Depends(get_user_repository),
):
    return SessionController(user_repository)
