from app.controllers.base import BaseController
from app.exceptions.user import UserAlreadyRegisteredException
from app.models import User
from app.repositories.user import UserRepository
from app.schemas.users import UserCreate, UserUpdate


class UserController(
    BaseController[User, UserRepository, UserCreate, UserUpdate]
):
    def create(self, create: UserCreate):
        found_user = self.repository.get_by_email(create.email)

        if found_user:
            raise UserAlreadyRegisteredException(email=create.email)

        return super().create(create)
