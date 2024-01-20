from sqlalchemy.orm import Session

from app.exceptions.user import UserNotFoundException
from app.models import User
from app.repositories.user import UserRepository


class SessionController:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(User, session)

    def login(self, email: str, password: str):
        found_user = self.user_repository.get_by_email(email)

        if not found_user:
            raise UserNotFoundException(email)
