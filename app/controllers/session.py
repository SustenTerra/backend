from sqlalchemy.orm import Session

from app.exceptions.user import UserPasswordDoNotMatchException
from app.hashing import Hasher
from app.models import User
from app.repositories.user import UserRepository


class SessionController:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login(self, email: str, password: str):
        found_user = self.user_repository.get_by_email(email)

        if not found_user:
            raise UserPasswordDoNotMatchException()

        if not Hasher.verify_password(password, found_user.password):
            raise UserPasswordDoNotMatchException()
