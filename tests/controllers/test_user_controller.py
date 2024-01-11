import pytest

from app.controllers.user import UserController
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.users import UserCreate


class TestUserController:
    @pytest.fixture
    def setup(self, db_session):
        self.repository = UserRepository(User, db_session)
        self.controller = UserController(User, self.repository)

    def test_create_user(self, setup, faker):
        create = UserCreate(
            email=faker.email(),
            full_name=faker.name(),
            password=faker.password(),
        )

        user = self.controller.create(create)

        assert user.id is not None
        assert user.email == create.email
        assert user.full_name == create.full_name

        found_user = self.repository.get_by_id(user.id)
        assert found_user is not None
