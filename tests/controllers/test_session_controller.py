import pytest
from fastapi.security import HTTPAuthorizationCredentials

from app.controllers.session import SessionController
from app.hashing import Hasher
from app.models import User
from app.repositories.user import UserRepository
from app.services.auth import get_logged_user


class TestSessionController:
    @pytest.fixture
    def setup(self, db_session, make_user):
        self.user_repository = UserRepository(User, db_session)
        self.controller = SessionController(self.user_repository)

        self.user_password = "12345678"
        self.created_user: User = make_user(
            email="davi@email.com",
            password=Hasher.get_password_hash(self.user_password),
        )
        self.user_repository.add(self.created_user)

    def test_make_login(self, setup):
        login = self.controller.login(
            self.created_user.email,
            self.user_password,
        )

        assert login is not None
        assert login.token is not None
        assert login.user is not None
        assert login.user.id == self.created_user.id
        assert login.user.email == self.created_user.email
        assert login.user.full_name == self.created_user.full_name
        assert login.user.phone == self.created_user.phone

        auth = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=login.token,
        )
        logged_user = get_logged_user(auth, self.user_repository)
        assert logged_user is not None
        assert logged_user.id == self.created_user.id
