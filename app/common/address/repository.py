from typing import Optional

from app.common.base.repository import BaseRepository
from app.models import Address


class AddressRepository(BaseRepository[Address]):
    def get_address_by_user_id(self, user_id: int) -> Optional[Address]:
        return self.default_query.filter_by(user_id=user_id).first()
