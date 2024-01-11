import pytest

from app.controllers.user import UserController
from app.models import User
from app.repositories.user import UserRepository
from app.schemas.users import UserCreate, UserUpdate


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

    def test_get_user(self, setup, faker):
        create = UserCreate(
            email=faker.email(),
            full_name=faker.name(),
            password=faker.password(),
        )

        user = self.controller.create(create)

        found_user = self.controller.get_by_id(user.id)
        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.email == user.email
        assert found_user.full_name == user.full_name

    def test_get_all_users(self, setup, faker):
        create = UserCreate(
            email=faker.email(),
            full_name=faker.name(),
            password=faker.password(),
        )

        user = self.controller.create(create)

        found_users = self.controller.get_all()
        assert len(found_users) == 1
        assert found_users[0].id == user.id
        assert found_users[0].email == user.email
        assert found_users[0].full_name == user.full_name

    def test_update_user(self, setup, faker):
        create = UserCreate(
            email=faker.email(),
            full_name=faker.name(),
            password=faker.password(),
        )

        user = self.controller.create(create)

        update = UserUpdate(
            email=faker.email(),
            full_name=faker.name(),
            password=faker.password(),
        )

        updated_user = self.controller.update(user.id, update)
        assert updated_user is not None
        assert updated_user.id == user.id
        assert updated_user.email == update.email
        assert updated_user.full_name == update.full_name

        found_user = self.repository.get_by_id(user.id)
        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.email == update.email
        assert found_user.full_name == update.full_name

    def test_delete_user(self, setup, faker):
        create = UserCreate(
            email=faker.email(),
            full_name=faker.name(),
            password=faker.password(),
        )

        user = self.controller.create(create)

        self.controller.delete(user.id)

        found_user = self.repository.get_by_id(user.id)
        assert found_user is None
