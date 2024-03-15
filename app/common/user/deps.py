from fastapi import Depends
from sqlalchemy.orm import Session

from app.common.user.content_status import UserContentStatusRepository
from app.common.user.controller import UserController
from app.common.user.repository import UserRepository
from app.deps import get_session
from app.models import User, UserContentStatus


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
