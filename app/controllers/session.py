from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app.config import Config
from app.exceptions.user import UserPasswordDoNotMatchException
from app.hashing import Hasher
from app.repositories.user import UserRepository
from app.schemas.sessions import LoginView
from app.schemas.users import UserView

config = Config()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class SessionController:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def _create_access_token(self, data: dict, expires_delta: timedelta):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM
        )
        return encoded_jwt

    def login(self, email: str, password: str):
        found_user = self.user_repository.get_by_email(email)

        if not found_user:
            raise UserPasswordDoNotMatchException()

        if not Hasher.verify_password(password, found_user.password):
            raise UserPasswordDoNotMatchException()

        access_token_expires = timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = self._create_access_token(
            data={"sub": str(found_user.id)},
            expires_delta=access_token_expires,
        )

        return LoginView(
            user=UserView.model_validate(found_user, from_attributes=True),
            token=access_token,
        )
