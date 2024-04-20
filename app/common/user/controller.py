from app.common.base.controller import BaseController
from app.common.user.exception import (
    UserAlreadyRegisteredException,
    UserIdNotFoundException,
    UserPasswordDoNotMatchException,
)
from app.common.user.repository import UserRepository
from app.common.user.schema import UserCreate, UserUpdate, UserUpdatePassword, UserView
from app.models import User
from app.service.hashing import Hasher


class UserController(BaseController[User, UserRepository, UserCreate, UserUpdate]):
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

    def get_by_id(self, id: int) -> UserView:
        found_user = self.repository.get_by_id(id)
        if not found_user:
            raise UserIdNotFoundException()

        return found_user
