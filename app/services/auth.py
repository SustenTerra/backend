from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jose import JWTError, jwt

from app.config import Config
from app.deps import get_user_repository
from app.repositories.user import UserRepository

config = Config()
apikey_scheme = APIKeyHeader(name="Authorization", scheme_name="Bearer")


def get_current_user(
    token: Annotated[str, Depends(apikey_scheme)],
    user_repository: UserRepository = Depends(get_user_repository),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, config.SECRET_KEY, algorithms=[config.ALGORITHM]
        )

        user_id = int(payload.get("sub", -1))
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    user = user_repository.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user
