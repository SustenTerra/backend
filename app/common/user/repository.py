from typing import Optional

from app.common.base.repository import BaseRepository
from app.models import User


class UserRepository(BaseRepository[User]):
    def get_by_email(self, email: str) -> Optional[User]:
        return self.default_query.filter_by(email=email).first()
