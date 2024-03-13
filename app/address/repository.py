from typing import Optional
from app.models import Address
from app.base.repository import BaseRepository


class AddressRepository(BaseRepository[Address]):
    def get_user_id(self, user_id: int) -> Optional[int]:
        return self.default_query.filter_by(user_id=user_id).first()

    def get_address_by_user_id(self, user_id: int) -> Optional[Address]:
        return self.default_query.filter_by(user_id=user_id).first()
