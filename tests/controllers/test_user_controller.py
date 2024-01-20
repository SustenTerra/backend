import pytest

from app.controllers.user import UserController
from app.models import User
from app.repositories.user import UserRepository
from app.schemas.users import UserCreate, UserUpdate, UserUpdatePassword
from app.hashing import Hasher


class TestUserController:
    @pytest.fixture
    def setup(self, db_session, make_user):
        self.repository = UserRepository(User, db_session)
        self.controller = UserController(User, self.repository)

        self.created_user: User = make_user()
        self.repository.add(self.created_user)

    def test_create_user(self, setup, faker):
        create = UserCreate(
            email=faker.email(),
            full_name=faker.name(),
            password=faker.password(),
            phone="83940028922",
        )

        user = self.controller.create(create)

        assert user.id is not None
        assert user.email == create.email
        assert user.full_name == create.full_name

        found_user = self.repository.get_by_id(user.id)
        assert found_user is not None

    def test_get_user(self, setup):
        found_user = self.controller.get_by_id(self.created_user.id)
        assert found_user is not None
        assert found_user.id == self.created_user.id
        assert found_user.email == self.created_user.email
        assert found_user.full_name == self.created_user.full_name

    def test_get_all_users(self, setup):
        found_users = self.controller.get_all()
        assert len(found_users) == 1
        assert found_users[0].id == self.created_user.id
        assert found_users[0].email == self.created_user.email
        assert found_users[0].full_name == self.created_user.full_name

    def test_update_user(self, setup, faker):
        update = UserUpdate(
            email=faker.email(),
            full_name=faker.name(),
            phone="83940028923",
        )

        updated_user = self.controller.update(self.created_user.id, update)
        assert updated_user is not None
        assert updated_user.id == self.created_user.id
        assert updated_user.email == update.email
        assert updated_user.full_name == update.full_name
        assert updated_user.phone == update.phone

        found_user = self.repository.get_by_id(self.created_user.id)
        assert found_user is not None
        assert found_user.id == self.created_user.id
        assert found_user.email == update.email
        assert found_user.full_name == update.full_name
        assert found_user.phone == update.phone


    def test_update_user_password(self, setup, faker, make_user):
        old_password = faker.password()
        user: User = make_user(password=Hasher.get_password_hash(old_password))
        self.repository.add(user)
        
        new_password = faker.password()

        update = UserUpdatePassword(
            current_password=old_password,
            password=new_password
        )

        updated_user = self.controller.update_password(user.id, update)
        assert updated_user is not None
        assert updated_user.id == user.id
        
        found_user = self.repository.get_by_id(user.id)
        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.email == user.email
        assert found_user.full_name == user.full_name
        assert found_user.phone == user.phone
        assert Hasher.verify_password(new_password, found_user.password)

    def test_delete_user(self, setup):
        self.controller.delete(self.created_user.id)

        found_user = self.repository.get_by_id(self.created_user.id)
        assert found_user is None
