from typing import Optional

from app.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def get_by_email(self, email: str) -> Optional[User]:
        return self.default_query.filter_by(email=email).first()