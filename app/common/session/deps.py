from fastapi import Depends

from app.common.session.controller import SessionController
from app.common.user.deps import get_user_repository
from app.common.user.repository import UserRepository


def get_session_controller(
    user_repository: UserRepository = Depends(get_user_repository),
):
    return SessionController(user_repository)
