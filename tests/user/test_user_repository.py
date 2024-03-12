import pytest

from app.models import User
from app.user.repository import UserRepository


class TestUserRepository:
    @pytest.fixture
    def setup(self, db_session, make_user):
        self.repository = UserRepository(User, db_session)

        self.created_user1: User = make_user()
        self.created_user2: User = make_user()
        self.repository.add(self.created_user1)
        self.repository.add(self.created_user2)

    def test_get(self, setup):
        found_user = self.repository.get().first()

        assert found_user is not None
        assert found_user.id == self.created_user1.id
        assert found_user.email == self.created_user1.email
        assert found_user.full_name == self.created_user1.full_name

    def test_get_all(self, setup):
        found_users = self.repository.get_all()

        assert len(found_users) == 2

    def test_get_by_id(self, setup):
        found_user = self.repository.get_by_id(2)

        assert found_user is not None
        assert found_user.id == self.created_user2.id
        assert found_user.email == self.created_user2.email
        assert found_user.full_name == self.created_user2.full_name

    def test_get_by_id_nonexistent(self, setup):
        found_user = self.repository.get_by_id(5)

        assert found_user is None

    def test_get_by_email(self, setup):
        found_user = self.repository.get_by_email(self.created_user2.email)

        assert found_user is not None
        assert found_user.id == self.created_user2.id
        assert found_user.email == self.created_user2.email
        assert found_user.full_name == self.created_user2.full_name

    def test_get_by_email_nonexistent(self, setup):
        found_user = self.repository.get_by_email("test@gmail.com")

        assert found_user is None

    def test_update(self, setup):
        new_email = "test@example.com"
        found_user = self.repository.update(2, {"email": new_email})

        assert found_user is not None
        assert found_user.id == self.created_user2.id
        assert found_user.email == new_email
        assert found_user.full_name == self.created_user2.full_name

    def test_delete(self, setup):
        self.repository.delete(2)

        found_users = self.repository.get_all()

        assert len(found_users) == 1
