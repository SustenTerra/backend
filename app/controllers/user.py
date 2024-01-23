from app.controllers.base import BaseController
from app.exceptions.user import (
    UserAlreadyRegisteredException,
    UserPasswordDoNotMatchException,
)
from app.hashing import Hasher
from app.models import User
from app.repositories.user import UserRepository
from app.schemas.users import UserCreate, UserUpdate, UserUpdatePassword


class UserController(
    BaseController[User, UserRepository, UserCreate, UserUpdate]
):
    def create(self, create: UserCreate):
        found_user = self.repository.get_by_email(create.email)

        if found_user:
            raise UserAlreadyRegisteredException(email=create.email)

        create.password = Hasher.get_password_hash(create.password)

        return super().create(create)

    def update(self, id, update: UserUpdate):
        if update.email:
            found_user = self.repository.get_by_email(update.email)

            if found_user:
                raise UserAlreadyRegisteredException(email=update.email)

        return super().update(id, update)

    def update_password(self, id, update: UserUpdatePassword):
        found_user = self.repository.get_by_id(id)

        if found_user and not Hasher.verify_password(
            update.current_password, found_user.password
        ):
            raise UserPasswordDoNotMatchException()

        update.new_password = Hasher.get_password_hash(update.new_password)

        return super().update(id, update, {"current_password"})  # type: ignore
